#Struts2 Content-Disposition filename null-byte variant of CVE-2017-5638
=======================================================================

[Struts2 Security Bulletin S2-046](https://cwiki.apache.org/confluence/display/WW/S2-046)

A null byte (`\x00`) in a request¡¯s `Content-Disposition` header filename field can trigger a `InvalidFileNameException` with the same (client controlled) filename string in the exception message that be used can trigger OGNL evaluation during error handling. Note that this is similar to but distinct from both the original [`Content-Type` vector reported in S2-045](https://cwiki.apache.org/confluence/display/WW/S2-045) and the [`Content-Length`/`Content-Disposition` variant](https://community.hpe.com/t5/Security-Research/Struts2-046-A-new-vector/ba-p/6949723#.WNA_5sDDFhE) also mentioned in [S2-046](https://cwiki.apache.org/confluence/display/WW/S2-046).

All the above variants are already fixed by the patches in Struts2 versions 2.3.32 and 2.5.10.1, and projects may alternatively use [struts-extras](https://github.com/apache/struts-extras) to do mitigation in-place without upgrading, but note that previous `Content-Type`-focused WAF/LB countermeasures may not protect against these alternative vectors.

```sh exploit-cd.sh [url] [command] [[add'l curl args]]```