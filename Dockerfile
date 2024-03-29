# 基本イメージを指定
FROM ubuntu:latest

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y openssh-server sudo

# SSH接続に必要な設定
RUN mkdir /var/run/sshd
RUN echo 'root:your_password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH接続時に必要な環境変数の設定
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# SSHサーバーの起動
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]