import json
import sys

# Add project paths so we can import both modules
sys.path.append('backend/app')
from risk import compute_priority as backend_compute
sys.path.append('aws_lambda/priority')
from app import compute_priority as lambda_compute


def load_sample():
    with open('aws_lambda/priority/sample-event.json') as f:
        return json.load(f)


def main():
    payload = load_sample()
    b = backend_compute(payload)
    l = lambda_compute(payload)
    if b == l:
        print('✅ Lambda output matches backend compute_priority')
        sys.exit(0)
    else:
        print('❌ Mismatch!')
        print('Backend:', b)
        print('Lambda :', l)
        sys.exit(1)

if __name__ == '__main__':
    main()
