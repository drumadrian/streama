

# Notes:
# https://streamaserver.org/getting-started/installing/
# https://serverfault.com/questions/664643/how-can-i-upgrade-to-java-1-8-on-an-amazon-linux-server
# https://gist.github.com/rtfpessoa/17752cbf7156bdf32c59


# https://github.com/s3fs-fuse/s3fs-fuse/wiki/Installation-Notes
# https://aws.amazon.com/premiumsupport/knowledge-center/ec2-enable-epel/
# https://github.com/s3fs-fuse/s3fs-fuse
# https://github.com/s3fs-fuse/s3fs-fuse/issues/744
# https://streamaserver.org/config/databases/

# https://www.youtube.com/watch?v=cAEtjMI1KcQ


# Run this script as the user: ec2-user


sudo yum update -y
sudo yum remove java-1.7.0-openjdk
sudo yum install -y git

# install jdk 8
cd /home/ec2-user
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie;" https://download.oracle.com/otn-pub/java/jdk/8u201-b09/42970487e3af4f5aa5bca3f542482c60/jdk-8u201-linux-x64.rpm
sudo rpm -i jdk-8u201-linux-x64.rpm 


java -version


wget https://github.com/streamaserver/streama/releases/download/v1.6.1/streama-1.6.1.war
chmod +x streama-1.6.1.war



# setup s3fs (may need to be run as root)
sudo yum-config-manager --enable epel
sudo yum repolist


sudo sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/epel.repo
sudo yum install -y gcc libstdc++-devel gcc-c++ fuse fuse-devel curl-devel libxml2-devel mailcap automake openssl-devel git
git clone https://github.com/s3fs-fuse/s3fs-fuse
cd s3fs-fuse/
./autogen.sh
./configure --prefix=/usr --with-openssl
make
sudo make install


mkdir /home/ec2-user/s3bucket
s3fs netflixadrianwscom /home/ec2-user/s3bucket -o iam_role="EC2_FULL_access_to_S3" -o url="https://s3-us-west-2.amazonaws.com" -o endpoint=us-west-2 -o dbglevel=info -o curldbg -o use_cache=/tmp





# Start Streama
bg java -jar streama-1.6.1.war
