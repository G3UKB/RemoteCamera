raspivid -o - -t 0 -hf -w 1024 -h 768 -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264
