import unittest
from unittest.mock import Mock, patch
import dns.resolver
from datetime import datetime
from pathlib import Path
import json
import os

from email_validator import EnhancedEmailValidator, ValidationScore, RateLimiter

class EmailValidatorTests(unittest.TestCase):
    """Test suite for EnhancedEmailValidator"""
    
    def setUp(self):
        self.test_cache_file = 'test_cache.json'
        self.validator = EnhancedEmailValidator(cache_file=self.test_cache_file)

    def tearDown(self):
        # Clean up test cache file
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)

    def test_format_score(self):
        """Test email format scoring"""
        test_cases = [
            ('user@example.com', 15),
            ('user.name@example.com', 15),
            ('u@ex.com', 10),
            ('invalid.email', 0),
            ('very.long.email.address.123456@really.long.domain.com', 10),
            ('no@spam!.com', 0)
        ]
        for email, expected_score in test_cases:
            with self.subTest(email=email):
                score = self.validator.calculate_format_score(email)
                self.assertEqual(score, expected_score)

    def test_domain_score(self):
        """Test domain pattern scoring"""
        test_cases = [
            ('example.com', 10),
            ('123.com', 5),
            ('very-long-domain-name-123.com', 7),
            ('multiple--hyphens.com', 7)
        ]
        for domain, expected_score in test_cases:
            with self.subTest(domain=domain):
                score = self.validator.calculate_domain_score(domain)
                self.assertEqual(score, expected_score)

    @patch('dns.resolver.Resolver.resolve')
    def test_mx_records(self, mock_resolve):
        """Test MX record verification"""
        # Mock MX records
        mock_records = [
            Mock(preference=10, exchange='mx1.example.com'),
            Mock(preference=20, exchange='mx2.example.com')
        ]
        mock_resolve.return_value = mock_records

        score, records, message = self.validator.verify_mx_records_with_score('example.com')
        self.assertGreater(score, 0)
        self.assertEqual(len(records), 2)
        self.assertIn("successfully", message)

    @patch('requests.head')
    def test_web_presence(self, mock_head):
        """Test web presence validation"""
        mock_response = Mock(
            status_code=200,
            url='https://example.com',
            headers={'content-type': 'text/html'},
            text='Welcome to our website'
        )
        mock_head.return_value = mock_response

        score = self.validator.check_web_presence('example.com')
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 15)

    @patch('whois.whois')
    def test_domain_age(self, mock_whois):
        """Test domain age estimation"""
        mock_whois.return_value = Mock(
            creation_date=datetime(2010, 1, 1),
            registrar='Test Registrar',
            emails=['admin@example.com']
        )

        score = self.validator.estimate_domain_age('example.com')
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 15)

    def test_rate_limiter(self):
        """Test rate limiter functionality"""
        limiter = RateLimiter(max_requests=2, time_window=1, burst_limit=3)
        domain = 'example.com'
        
        self.assertTrue(limiter.can_make_request(domain))
        self.assertTrue(limiter.can_make_request(domain))
        self.assertFalse(limiter.can_make_request(domain))

    def test_cache_functionality(self):
        """Test caching of validation results"""
        test_email = "test@example.com"
        
        # First validation should not use cache
        result1 = self.validator.verify_email_with_score(test_email)
        
        # Modify cache to ensure we're reading from it
        self.validator.cache[test_email]['score'] = 99.9
        
        # Second validation should use cache
        result2 = self.validator.verify_email_with_score(test_email)
        
        self.assertNotEqual(result1.score, result2.score)
        self.assertEqual(result2.score, 99.9)

    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_parallel_execution(self, mock_executor):
        """Test parallel execution of validation checks"""
        mock_executor.return_value.__enter__.return_value = Mock()
        
        self.validator.verify_email_with_score('test@example.com')
        
        # Verify that ThreadPoolExecutor was used
        mock_executor.assert_called_once()

    def test_validation_score_creation(self):
        """Test ValidationScore creation and attributes"""
        score = ValidationScore(
            score=75.5,
            valid=True,
            confidence="High",
            details={'format': 15, 'mx_records': 25},
            message="Test validation"
        )
        
        self.assertEqual(score.score, 75.5)
        self.assertTrue(score.valid)
        self.assertEqual(score.confidence, "High")
        self.assertEqual(score.details['format'], 15)
        self.assertEqual(score.message, "Test validation")

if __name__ == '__main__':
    unittest.main(verbosity=2)