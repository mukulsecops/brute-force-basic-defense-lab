import logging, time

# Security Configs
MAX_ATTEMPTS=5
BLOCK_TIME=120 # in seconds.
RATE_LIMIT_WINDOW=30
RATE_LIMIT_MAX=10

failed_attempts={}
blocked_ips = {}
request_log = {}

# Logging
auth_logger = logging.getLogger("auth_logger")
auth_logger.setLevel(logging.INFO)

handler = logging.FileHandler("logs/auth.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

handler.setFormatter(formatter)
auth_logger.addHandler(handler)


# -----------------------------
# SECURITY FUNCTIONS
# -----------------------------

def is_ip_blocked(ip):
    """Check if IP is temporarly blocked!"""
    if ip in blocked_ips:
        if time.time() < blocked_ips[ip]:
            return True
        else:
            del blocked_ips[ip]
    return False


def check_rate_limit(ip):
    """Basic rate limiting"""
    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [
        t for t in request_log[ip]
        if now - t < RATE_LIMIT_WINDOW
    ]

    request_log[ip].append(now)
    return len(request_log[ip]) <= RATE_LIMIT_MAX


def track_failed_attempt(ip):
    """Track failed login attempts"""
    failed_attempts[ip] =  failed_attempts.get(ip, 0) + 1

    if failed_attempts[ip] >= MAX_ATTEMPTS:
        blocked_ips[ip] = time.time() + BLOCK_TIME
        auth_logger.warning(f"[IP_BLOCKED] | IP={ip}")
        failed_attempts[ip] = 0


def auth_log_success(ip, username):
    auth_logger.info(f"[AUTH_SUCCESS] | IP={ip} | USERNAME={username}")


def auth_log_failure(ip, username):
    auth_logger.warning(f"[AUTH_FAIL] | IP={ip} | USERNAME={username}")

def ip_block_attempt_log(ip):
    auth_logger.warning(f"[BLOCKED_ATTEMPT] | IP={ip}")

def rate_limit_log(ip):
    auth_logger.warning(f"[RATE_LIMIT] | IP={ip}")
