systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent


echo "Setting up Blender instance..."
cd ~
git clone https://github.com/arachtivix/mathstudynotes
cd mathstudynotes/chess/blender

sudo sh install-bender.sh

echo "Installing Blender..."
sudo sh install-bender.sh

echo "Syncing assets from S3 bucket"
mkdir -p assets
aws s3 sync s3://wernerware-blender-assets ./assets/
