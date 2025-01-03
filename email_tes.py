# email_tes.py

# import re
# import smtplib
# import dns.resolver
# from typing import Tuple, Optional, Dict, List, NamedTuple
# import socket
# import logging
# import ssl
# from datetime import datetime, timedelta
# import json
# from pathlib import Path
# import threading
# from collections import defaultdict
# import requests
# from urllib.parse import urlparse

# class RateLimiter:
#     """Rate limiter to prevent server flooding"""
#     def __init__(self, max_requests: int = 5, time_window: int = 60):
#         self.max_requests = max_requests
#         self.time_window = time_window
#         self.requests = defaultdict(list)
#         self.lock = threading.Lock()

#     def can_make_request(self, domain: str) -> bool:
#         with self.lock:
#             now = datetime.now()
#             self.requests[domain] = [req_time for req_time in self.requests[domain] 
#                                    if now - req_time < timedelta(seconds=self.time_window)]
#             if len(self.requests[domain]) < self.max_requests:
#                 self.requests[domain].append(now)
#                 return True
#             return False

# class ValidationScore(NamedTuple):
#     score: float
#     valid: bool
#     confidence: str
#     details: Dict[str, float]
#     message: str

# class EnhancedEmailValidator:
#     def __init__(self, from_address: str = 'verify@example.com', cache_file: str = 'email_cache.json'):
#         self.from_address = from_address
#         self.cache_file = Path(cache_file)
#         self.logger = logging.getLogger(__name__)
#         self.rate_limiter = RateLimiter(max_requests=10, time_window=60)
        
#         # Scoring weights (total = 100)
#         self.weights = {
#             'format': 15,            # Basic email format
#             'domain_pattern': 10,    # Domain structure
#             'mx_records': 25,        # MX record validity
#             'domain_age': 15,        # Age of the domain
#             'company_match': 20,     # Company name matches domain
#             'web_presence': 15       # Website existence and validity
#         }
        
#         # Business email providers
#         self.business_providers = [
#             'outlook.com', 'office365.com', 'microsoft.com',
#             'google.com', 'googlemail.com', 'zoho.com'
#         ]
        
#         # Initialize other components
#         self.initialize_components()

#     def load_cache(self) -> None:
#         """Load validation cache from file"""
#         try:
#             if self.cache_file.exists():
#                 with open(self.cache_file, 'r') as f:
#                     cache_data = json.load(f)
#                     now = datetime.now()
#                     self.cache = {}
#                     for email, data in cache_data.items():
#                         # Convert the timestamp string back to datetime
#                         data['timestamp'] = datetime.fromisoformat(data['timestamp'])
#                         if data['timestamp'] + timedelta(days=1) > now:
#                             self.cache[email] = data
#         except Exception as e:
#             self.logger.error(f"Error loading cache: {e}")
#             self.cache = {}

#     def save_cache(self) -> None:
#         """Save validation cache to file"""
#         try:
#             # Convert datetime objects to ISO format strings for JSON serialization
#             cache_data = {
#                 email: {
#                     'validation_result': {
#                         'score': data['validation_result'].score,
#                         'valid': data['validation_result'].valid,
#                         'confidence': data['validation_result'].confidence,
#                         'details': data['validation_result'].details,
#                         'message': data['validation_result'].message
#                     },
#                     'timestamp': data['timestamp'].isoformat()
#                 }
#                 for email, data in self.cache.items()
#             }
#             with open(self.cache_file, 'w') as f:
#                 json.dump(cache_data, f)
#         except Exception as e:
#             self.logger.error(f"Error saving cache: {e}")

#     def initialize_components(self):
#         """Initialize validator components"""
#         self.ssl_context = ssl.create_default_context()
#         self.cache = {}
#         self.load_cache()

#     def calculate_format_score(self, email: str) -> float:
#         """Calculate score for email format validity"""
#         score = 0
#         if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
#             score += 10
            
#             # Additional format checks
#             local_part = email.split('@')[0]
#             if 2 < len(local_part) < 32:  # Reasonable length
#                 score += 5
#             if not re.search(r'[._%+-]{2,}', local_part):  # No consecutive special chars
#                 score += 5
            
#         return min(score, 15)  # Cap at 15 points

#     def calculate_domain_score(self, domain: str) -> float:
#         """Calculate score for domain validity"""
#         score = 0
#         try:
#             # Basic domain pattern
#             if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$', domain):
#                 score += 5
            
#             # Check domain parts
#             parts = domain.split('.')
#             if 2 <= len(parts) <= 4:
#                 score += 3
            
#             # Length checks
#             if len(domain) < 255 and all(len(p) < 63 for p in parts):
#                 score += 2
                
#         except Exception:
#             return 0
            
#         return min(score, 10)

#     def verify_mx_records_with_score(self, domain: str) -> Tuple[float, List[Tuple[int, str]], str]:
#         """Verify MX records and return a score"""
#         try:
#             resolver = dns.resolver.Resolver()
#             resolver.timeout = 10
            
#             mx_records = resolver.resolve(domain, 'MX')
#             records = sorted([(r.preference, str(r.exchange)) for r in mx_records])
            
#             score = 0
#             mx_servers = [mx[1].lower() for mx in records]
            
#             # Basic MX existence
#             if records:
#                 score += 15
                
#                 # Check for business providers
#                 if any(provider in mx for mx in mx_servers for provider in self.business_providers):
#                     score += 5
                
#                 # Multiple MX records
#                 if len(records) > 1:
#                     score += 5
                
#                 # Properly configured preferences
#                 if all(0 <= pref <= 65535 for pref, _ in records):
#                     score += 5
                
#             return min(score, 25), records, "MX records found and analyzed"
            
#         except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
#             return 0, [], "No MX records found"
#         except dns.exception.DNSException as e:
#             return 0, [], f"DNS error: {str(e)}"

#     def check_web_presence(self, domain: str) -> float:
#         """Check website existence and validity"""
#         score = 0
#         try:
#             # Try HTTPS first
#             response = requests.head(f'https://{domain}', timeout=5, allow_redirects=True)
#             if response.status_code == 200:
#                 score += 10
#                 if response.url.startswith('https'):
#                     score += 5
#             elif response.status_code < 500:  # Any valid response
#                 score += 5
#         except requests.RequestException:
#             try:
#                 # Fallback to HTTP
#                 response = requests.head(f'http://{domain}', timeout=5, allow_redirects=True)
#                 if response.status_code == 200:
#                     score += 7
#                 elif response.status_code < 500:
#                     score += 3
#             except requests.RequestException:
#                 pass
        
#         return min(score, 15)

#     def estimate_domain_age(self, domain: str) -> float:
#         """Estimate domain age and popularity"""
#         score = 0
#         try:
#             # WHOIS lookup simulation (you'd want to use a proper WHOIS library)
#             resolver = dns.resolver.Resolver()
#             resolver.timeout = 5
            
#             # Try to resolve various records
#             try:
#                 resolver.resolve(domain, 'A')
#                 score += 5
#             except Exception:
#                 pass
                
#             try:
#                 resolver.resolve(domain, 'MX')
#                 score += 5
#             except Exception:
#                 pass
                
#             try:
#                 resolver.resolve(f'www.{domain}', 'A')
#                 score += 5
#             except Exception:
#                 pass
                
#         except Exception:
#             pass
            
#         return min(score, 15)

#     def analyze_company_match(self, email: str, domain: str) -> float:
#         """Analyze if email matches company pattern"""
#         score = 0
        
#         # Extract potential company name from domain
#         company_name = domain.split('.')[0].lower()
#         local_part = email.split('@')[0].lower()
        
#         # Common business email patterns
#         if re.match(r'^[a-z]+\.[a-z]+$', local_part):  # firstname.lastname
#             score += 10
#         elif re.match(r'^[a-z]\.[a-z]+$', local_part):  # f.lastname
#             score += 8
#         elif re.match(r'^[a-z]+$', local_part):  # username
#             score += 5
            
#         # Check for department or role-based emails
#         common_roles = {'info', 'support', 'sales', 'admin', 'contact', 'hr'}
#         if local_part in common_roles:
#             score += 10
            
#         return min(score, 20)

#     def verify_email_with_score(self, email: str) -> ValidationScore:
#         """Verify email with detailed scoring"""
#         # Check cache first
#         if email in self.cache:
#             cache_entry = self.cache[email]
#             if datetime.now() - cache_entry['timestamp'] < timedelta(days=1):
#                 return ValidationScore(
#                     score=cache_entry['score'],
#                     valid=cache_entry['valid'],
#                     confidence=cache_entry['confidence'],
#                     details=cache_entry['details'],
#                     message=cache_entry['message']
#                 )

#         email = email.lower().strip()
        
#         # Initialize scores dictionary
#         scores = {
#             'format': 0,
#             'domain_pattern': 0,
#             'mx_records': 0,
#             'domain_age': 0,
#             'company_match': 0,
#             'web_presence': 0
#         }
        
#         try:
#             _, domain = email.split('@')
#         except ValueError:
#             return ValidationScore(0, False, "Very Low", scores, "Invalid email format")
            
#         # Calculate individual scores
#         scores['format'] = self.calculate_format_score(email)
#         scores['domain_pattern'] = self.calculate_domain_score(domain)
        
#         mx_score, _, _ = self.verify_mx_records_with_score(domain)
#         scores['mx_records'] = mx_score
        
#         scores['domain_age'] = self.estimate_domain_age(domain)
#         scores['company_match'] = self.analyze_company_match(email, domain)
#         scores['web_presence'] = self.check_web_presence(domain)
        
#         # Calculate total weighted score
#         total_score = sum(scores[k] * self.weights[k] / max(self.weights.values()) 
#                         for k in scores.keys())
        
#         # Determine confidence level and validity
#         if total_score >= 80:
#             confidence = "Very High"
#             valid = True
#         elif total_score >= 65:
#             confidence = "High"
#             valid = True
#         elif total_score >= 50:
#             confidence = "Medium"
#             valid = True
#         elif total_score >= 35:
#             confidence = "Low"
#             valid = False
#         else:
#             confidence = "Very Low"
#             valid = False
            
#         # Generate detailed message
#         message = f"Email validation score: {total_score:.1f}/100 ({confidence} confidence)"
        
#         validation_result = ValidationScore(total_score, valid, confidence, scores, message)
        
#         # Unpack ValidationScore for caching
#         self.cache[email] = {
#             'score': validation_result.score,
#             'valid': validation_result.valid,
#             'confidence': validation_result.confidence,
#             'details': validation_result.details,
#             'message': validation_result.message,
#             'timestamp': datetime.now()
#         }
#         self.save_cache()
        
#         return validation_result
        
# def main():
#     """Main function to run email verification"""
#     logging.basicConfig(level=logging.INFO)
#     validator = EnhancedEmailValidator()
    
#     print("Enhanced Email Validator (type 'quit' to exit)")
#     print("Note: This tool provides detailed scoring for email validity")
    
#     while True:
#         email = input('\nEnter email address to verify: ').strip()
        
#         if email.lower() == 'quit':
#             break
            
#         print("\nAnalyzing email...")
#         result = validator.verify_email_with_score(email)
        
#         print(f"\nValidation Results for {email}:")
#         print(f"Overall Score: {result.score:.1f}/100")
#         print(f"Validity: {'Valid' if result.valid else 'Invalid'}")
#         print(f"Confidence: {result.confidence}")
#         print("\nDetailed Scores:")
#         for category, score in result.details.items():
#             print(f"- {category.replace('_', ' ').title()}: {score:.1f}")
#         print(f"\nMessage: {result.message}")

# if __name__ == "__main__":
#     main()
    
################################################################################
import re
import smtplib
import dns.resolver
from typing import Tuple, Optional, Dict, List, NamedTuple, Union
import socket
import logging
import ssl
from datetime import datetime, timedelta
import json
from pathlib import Path
import threading
from collections import defaultdict
import requests
from urllib.parse import urlparse
import backoff
import whois
import concurrent.futures

class ValidationScore(NamedTuple):
    score: float
    valid: bool
    confidence: str
    details: Dict[str, float]
    message: str

class EnhancedEmailValidator:
    def __init__(self, 
                 dns_timeout: int = 10,
                 max_workers: int = 3):
        self.logger = logging.getLogger(__name__)
        self.dns_timeout = dns_timeout
        self.max_workers = max_workers
        
        # Adjusted weights to better differentiate valid from invalid emails
        self.weights = {
            'format': 20,           # Increased importance of format
            'domain_pattern': 15,   # Increased domain pattern weight
            'mx_records': 40,       # Slightly reduced but still most important
            'domain_type': 15,      # Slightly reduced
            'domain_age': 10        # Kept the same
        }
        
        # Expanded valid patterns with more common cases
        self.valid_patterns = [
            r'^[a-z]+\.[a-z]+@',           # first.last@
            r'^[a-z]+@',                   # firstname@
            r'^[a-z]\.[a-z]+@',            # f.last@
            r'^[a-z]+\.[a-z]+\.[a-z]+@',   # first.middle.last@
            r'^[a-z]+[0-9]{0,3}@',         # firstname123@ (up to 3 numbers)
            r'^[a-z]{1,2}\.[a-z]+@',       # fl.last@
            r'^[a-z]+[-_.][a-z]+@',        # first-last@ or first_last@
            r'^[a-z]+[-.][a-z]+[0-9]{0,2}@' # first.last01@
        ]
        
        # Expanded domain lists
        self.academic_domains = {
            'edu', 'ac.uk', 'edu.au', 'edu.cn', 'ac.nz', 'ac.jp', 'edu.sg',
            'ac.in', 'edu.hk', 'edu.my', 'edu.ph'
        }
        
        self.corporate_domains = {
            'com', 'co.uk', 'ltd.uk', 'plc.uk', 'com.au', 'co.nz', 'co.jp',
            'co.in', 'com.sg', 'com.hk', 'com.my', 'com.ph', 'org', 'net'
        }

    def calculate_format_score(self, email: str) -> float:
        """Improved format scoring"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return 0
            
        email = email.lower()
        score = 10  # Start with base score
        
        local_part, domain = email.split('@')
        
        # Length checks with graduated scoring
        if 2 <= len(local_part) <= 64 and 3 <= len(domain) <= 255:
            score += 10
            if 4 <= len(local_part) <= 32:  # Most common length range
                score += 5
        
        # Pattern matching with higher scores
        if any(re.match(pattern, email) for pattern in self.valid_patterns):
            score += 15
            
        # Reduced penalties
        penalties = [
            (local_part.count('.') > 2, 3),   # Allow more dots
            (re.match(r'^[0-9]', local_part), 3),  # Numbers at start less penalized
            (re.match(r'.*[.]{2,}.*', local_part), 7),  # Keep strict on double dots
            (re.match(r'.*[-_]{2,}.*', local_part), 3),  # Less penalty for multiple special chars
        ]
        
        for condition, penalty in penalties:
            if condition:
                score = max(0, score - penalty)
                
        return min(score, 20)  # Cap at maximum weight

    def calculate_domain_score(self, domain: str) -> float:
        """Enhanced domain pattern scoring"""
        score = 15  # Start with maximum score
        
        # Penalty factors with reduced impact
        penalties = [
            (re.search(r'\d{4,}', domain), 8),  # Multiple numbers
            (re.match(r'.*\.(xyz|top|website|space|site)$', domain), 8),  # Suspicious TLDs
            (len(domain) > 40, 8),  # Very long domains
            (domain.count('-') > 1, domain.count('-') * 2),  # Multiple hyphens
            (domain.count('.') > 3, 4),  # Too many subdomains
            (re.match(r'^[0-9]', domain), 4)  # Starts with number
        ]
        
        # Common TLD bonus
        common_tlds = {'com', 'org', 'net', 'edu', 'gov', 'mil', 'int'}
        if any(domain.endswith('.' + tld) for tld in common_tlds):
            score += 5
            
        # Apply penalties
        for condition, penalty in penalties:
            if condition:
                score = max(0, score - penalty)
                
        # Normalize to weight
        return min(score, 15)  # Cap at weight value

    def calculate_domain_type_score(self, domain: str) -> float:
        """Improved domain type scoring"""
        score = 5  # Start with base score
        domain_lower = domain.lower()
        
        # Graduated scoring based on domain type
        if any(domain_lower.endswith('.' + tld) for tld in self.academic_domains):
            score += 15
        elif domain_lower.endswith('.gov') or domain_lower.endswith('.gov.uk'):
            score += 15
        elif any(domain_lower.endswith('.' + tld) for tld in self.corporate_domains):
            score += 12
        else:
            score += 8  # Increased base score for other valid domains
            
        # Reduced penalties for suspicious patterns
        if re.search(r'\d{4,}', domain):
            score = max(0, score - 5)
        if domain.count('-') > 1:
            score = max(0, score - 3)
        if domain.count('.') > 2:
            score = max(0, score - 3)
            
        return min(score, 15)  # Cap at maximum weight

    def verify_mx_records_with_score(self, domain: str) -> Tuple[float, List[str], str]:
        """Significantly enhanced MX record scoring with better validation"""
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = self.dns_timeout
            
            mx_records = resolver.resolve(domain, 'MX')
            records = [(r.preference, str(r.exchange).rstrip('.').lower()) for r in mx_records]
            
            if not records:
                return 0, [], "No MX records found"
                
            score = 35  # Higher base score for having valid MX records
            
            # Enhanced provider scoring with more common business providers
            premium_providers = {
                # Major providers - highest trust
                'google': 20,
                'outlook': 20,
                'office365': 20,
                'microsoft': 20,
                'gmail': 20,
                'googlemail': 20,
                
                # Business and hosting providers - high trust
                'zoho': 18,
                'amazonses': 18,
                'mailgun': 18,
                'sendgrid': 18,
                'postmark': 18,
                'mailchimp': 18,
                'mandrill': 18,
                
                # Common email providers - medium-high trust
                'yahoo': 15,
                'hotmail': 15,
                'protonmail': 15,
                'aol': 15,
                'icloud': 15,
                
                # Generic hosting providers - medium trust
                'hostgator': 12,
                'godaddy': 12,
                'rackspace': 12,
                'dreamhost': 12,
                'bluehost': 12
            }
            
            # Check for business-specific MX patterns
            business_patterns = [
                r'mail\d*\..*\.com$',
                r'smtp\d*\..*\.com$',
                r'mx\d*\..*\.com$',
                r'aspmx\d*\..*\.com$',
                r'mailserver\d*\..*\.com$'
            ]
            
            # Check provider reputation with improved scoring
            provider_matched = False
            for mx in records:
                mx_domain = mx[1]
                
                # Check for premium providers
                for provider, bonus in premium_providers.items():
                    if provider in mx_domain:
                        score = min(score + bonus, 55)
                        provider_matched = True
                        break
                
                # If no premium provider matched, check for business patterns
                if not provider_matched:
                    for pattern in business_patterns:
                        if re.match(pattern, mx_domain):
                            score = min(score + 10, 55)  # Bonus for business-like setup
                            break
            
            # Verify MX server responsiveness
            success_count = 0
            for mx in records[:2]:  # Check first two MX records
                try:
                    primary_mx = mx[1]
                    socket.gethostbyname(primary_mx)
                    success_count += 1
                except socket.error:
                    continue
            
            if success_count > 0:
                score = min(score + 5 * success_count, 55)
            else:
                score = max(0, score - 10)
                
            return score, [r[1] for r in records], "MX records verified"
            
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            return 0, [], "No valid MX records found"
        except Exception as e:
            return 0, [], f"DNS error: {str(e)}"

    def estimate_domain_age(self, domain: str) -> float:
        """Improved domain age scoring"""
        try:
            domain_info = whois.whois(domain)
            
            if domain_info.creation_date:
                creation_date = (
                    domain_info.creation_date[0]
                    if isinstance(domain_info.creation_date, list)
                    else domain_info.creation_date
                )
                
                age_years = (datetime.now() - creation_date).days / 365
                
                # More granular scoring
                if age_years >= 15:
                    return 10
                elif age_years >= 10:
                    return 8
                elif age_years >= 5:
                    return 6
                elif age_years >= 2:
                    return 4
                elif age_years >= 1:
                    return 3
                    
                return 2
                
        except Exception:
            # Fallback DNS check with higher base scoring
            try:
                resolver = dns.resolver.Resolver()
                resolver.timeout = 5
                
                score = 2  # Start with base score
                for record_type in ['A', 'NS', 'SOA']:
                    try:
                        resolver.resolve(domain, record_type)
                        score += 2
                    except Exception:
                        pass
                return score
            except:
                return 0
            
        return 0

    def verify_email_with_score(self, email: str) -> ValidationScore:
        """Main verification method with domain-aware scoring"""
        email = email.lower().strip()
        
        try:
            local_part, domain = email.split('@')
        except ValueError:
            return ValidationScore(
                score=0.0,
                valid=False,
                confidence="Very Low",
                details={k: 0.0 for k in self.weights},
                message="Invalid email format"
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                'format': executor.submit(self.calculate_format_score, email),
                'domain_pattern': executor.submit(self.calculate_domain_score, domain),
                'mx_records': executor.submit(self.verify_mx_records_with_score, domain),
                'domain_type': executor.submit(self.calculate_domain_type_score, domain),
                'domain_age': executor.submit(self.estimate_domain_age, domain)
            }

            scores = {
                'format': futures['format'].result(),
                'domain_pattern': futures['domain_pattern'].result(),
                'mx_records': futures['mx_records'].result()[0],
                'domain_type': futures['domain_type'].result(),
                'domain_age': futures['domain_age'].result()
            }

        # Calculate weighted score
        total_score = sum(scores[k] * self.weights[k] / max(self.weights.values())
                         for k in scores.keys())
        
        # Adjusted scoring thresholds with focus on MX records
        mx_score = scores['mx_records']
        if total_score >= 70 and mx_score >= 40:
            confidence, valid = "Very High", True
        elif total_score >= 60 and mx_score >= 35:
            confidence, valid = "High", True
        elif total_score >= 50 and mx_score >= 30:
            confidence, valid = "Medium", True
        else:
            confidence, valid = "Low", False

        # Critical failures
        if mx_score < 20:  # Stricter MX requirement
            valid = False
            confidence = "Low"
            
        if mx_score == 0:  # No MX records = invalid
            valid = False
            confidence = "Very Low"
            total_score = max(total_score * 0.5, 20)

        message = f"Email validation score: {total_score:.1f}/100 ({confidence} confidence)"

        return ValidationScore(
            score=total_score,
            valid=valid,
            confidence=confidence,
            details=scores,
            message=message
        )
        
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    validator = EnhancedEmailValidator()
    
    while True:
        try:
            email = input('\nEnter email address to verify: ').strip()
            
            if email.lower() == 'quit':
                break
                
            print("\nAnalyzing email...")
            result = validator.verify_email_with_score(email)
            
            print(f"\nValidation Results for {email}:")
            print(f"Overall Score: {result.score:.1f}/100")
            print(f"Validity: {'Valid' if result.valid else 'Invalid'}")
            print(f"Confidence: {result.confidence}")
            print("\nDetailed Scores:")
            for category, score in result.details.items():
                print(f"- {category.replace('_', ' ').title()}: {score:.1f}")
            print(f"\nMessage: {result.message}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
# python email_tes.py
