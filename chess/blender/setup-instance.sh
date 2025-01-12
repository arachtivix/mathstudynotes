systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent

cd ~
git clone https://github.com/arachtivix/mathstudynotes
cd mathstudynotes/chess/blender

sudo sh install-bender.sh

mkdir -p assets
aws s3 sync s3://wernerware-blender-assets ./assets/
