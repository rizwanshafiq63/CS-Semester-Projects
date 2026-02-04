# 1. Generate keys
python keygen.py

# 2. Create a message file
echo "This is a secret message" > message.txt

# 3. Sign the message
python sign.py message.txt

# 4. Verify the signature
python verification.py message.txt
