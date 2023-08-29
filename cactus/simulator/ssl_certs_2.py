from __future__ import annotations

from typing import Dict, Tuple

SSL_TEST_PRIVATE_CA_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDKTCCAhGgAwIBAgIUbFhRlgpIM3M+ZYuTigQ1Vbmi6P4wDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMB4XDTIyMDMyMzE3MjkyMloXDTMyMDMy
MDE3MjkyMlowRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8G
A1UECwwYT3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMIIBIjANBgkqhkiG9w0BAQEF
AAOCAQ8AMIIBCgKCAQEAsc4R76dCSzj3MR7adSLI+Mk9cX42bTHiu00c964rUXr2
eGpYy1fmtdiq71kkVFRCtX+m8tc0jA5RCOCJsVKPZ7a2zQVcUkC1HJDCg8lufI2p
hS33zpjP+BePGmxQDhBU744cmFA/TVN+VTEhTlbmhFo62eX2Repbl2coF3MhoKTz
cilUgiCww+DUa6IQk06Zkh8TFJ8iPp67QRM1wEhMEcKrnRNxPGHDxa9ZxhwrmKft
UOFrat+ijftQDexMkVZLUXPoksM/7afjqvP9fkFpQEJZ3R1p3uwSX+oIr4yE/0il
nnLnunvUcWYTmvVcwrV5Zu+IOtV+yBbJxmFsobiecQIDAQABoxMwETAPBgNVHRMB
Af8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQAgxl6fGre+yFpKxEVcJ554klsg
Hefei1tv94BDMqdzfdeocTBiYmN70j9KEZr5CoMUhpRh0sESpgZ+6JD506Crpa6y
CwkhfQXwOH58E6pbqLLpG3F96BeIBQ/IS0iGvRaerK/9hybt4NJAyrXX1idJikiJ
h4qck731LOSiCw7T138yjlVEXm4DdCj/MYJDJJznMYDXJrJEE7tDHHvPaPU3Snrd
CeAYwXaZlvoCbU0f0DCyAXS5+/HgzY5qVrvDCACTAEnMSEQyIhESSL2xmumTGNCA
BBlbMJ6oLn3fOHrB7qQortCwcAQkbk/MiZhAkL/+NDz6gdIZqgXLDDVZxext
-----END CERTIFICATE-----
"""

SSL_TEST_PRIVATE_CA_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxzhHvp0JLOPcx
Htp1Isj4yT1xfjZtMeK7TRz3ritRevZ4aljLV+a12KrvWSRUVEK1f6by1zSMDlEI
4ImxUo9ntrbNBVxSQLUckMKDyW58jamFLffOmM/4F48abFAOEFTvjhyYUD9NU35V
MSFOVuaEWjrZ5fZF6luXZygXcyGgpPNyKVSCILDD4NRrohCTTpmSHxMUnyI+nrtB
EzXASEwRwqudE3E8YcPFr1nGHCuYp+1Q4Wtq36KN+1AN7EyRVktRc+iSwz/tp+Oq
8/1+QWlAQlndHWne7BJf6givjIT/SKWecue6e9RxZhOa9VzCtXlm74g61X7IFsnG
YWyhuJ5xAgMBAAECggEAGKUzn0BT1BFlUg2wwiO8L5/VQHH6IVCU2NlrdnlRz813
dGFpRWY9uF778oksm/PB+15iSa7CvdcOLGjTLR0Ae6O72tcvYMdPU1JNY+77vY/1
O1yPyLctvHmngEYbIpfo7fuIwyP8Yj98d1qD/1PUR+wp1CIn7LD7WRUXXYi71IRN
dVKX7G0S/QPSePe+9ILMd/fA8Qs0wOKBvWRHjfOxvNP9AXTeuUzLbbGQ1YPLGSLU
R2aS5T3f7wNAKyjmvk7AjeEYNDNZbZzmc+bj36buUd7dqlhTGOFt0sBZ/K+IQjnK
wiF/2rBFdklMePuqdyuRhkybjAjj1NZvfXxLD8TCcQKBgQDfTbUaDqWrB8vf76ZQ
pjIYQpXBEU8r1xlTr7ExP7KM+1qGdtGW54uln+tFgpR7mIgZg10ehCAuqwT2GHSJ
luOI0tDQcu8wG3RB0x7L4Xq8qXORKIEmyZ+ZleBAwjfq4du4lyb0Ob+dKjFBPSuY
eTWt1bSGklk61QoyWbVJ2NQf7wKBgQDL1uW1PKrygzBcnt2ndR8u1IvjLl6Q8t7y
j79wxM4eNpkEMV09eAU3cNAuquG88BAeXUY8j7OyMuhlgG2s6AgnQO3/g32OKNJ1
+F9m3CldxXFY9dKOH+FOZjb2kPcgNX2xvKo/IvGkxoIvwGtRc9OkvK65RSlqc/GH
MbkVezrHnwKBgQC2u6JdxmqvwNuHT1dsW/RWgfaGXaHKIGVrZDS+Nn/oerAjpQvy
T1yplmozIZ5cXf/R0PvcwwaK6gxPTsfe6AkeqFWUntk5Jt5GF3v2H3gO9yPJP7og
gZIHXux6UfTsUxM4xQhthuxUsnhICMSqK1ZQALeQACbgzAFiHqMJ4VQFJQKBgCS5
J5M6RdYBGpJlMKu9pwuJ0VXxgan9h3sNuMC5RCUfUvv1ZMXxPIdbdLYjpR2j5lOC
HGhGv2oIT+QRejDfcLCZuwcAins1EY2dXJqsaWtyadRMHU3romy8b4SGY29TE70U
r1tGkWBNPyEZOnxnMKcKMzQ/qJF8J/RiWeTr2ZAjAoGBALSW7/CRSwm1sxpQNbm/
TlehXDdz5od3d8VftZbXR3hoOrMVdgyN3FO0qmRjGkG6hyj0TU9kwXbjzAYywiW3
KTA+/LtAjeBFuxkhbqBPBQGwjfFNg7Ju7bG2t9U7qSw/Swihg4kfYlsl8jLPLj2E
D3THVwgDuL8d0lZEaK0n/EqT
-----END PRIVATE KEY-----
"""

SSL_TEST_FULLNODE_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUJBzmO7OHvvlimGi0mXLrh/8TPeMwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQC792uVfc1mFbJluKxzWxZ0r5yaKGjR8azECVrNTcegAjLF
Qd7+iZS+7DZwEA6Xy/h8T9DZd3Q1m0Rjlgg73ngO50leCvLqWEvrhueuEIWLdbef
4NaX4qkusMI/orYE/ItKgL86HWkGUELnmf3TkMccohR63vS+Fr6dZDvIw3g+gBPL
P9MlK7sdXq1I8CIcV+2du4jhmkA4mJ278TdQZOfXnX1hhe1wPuyhJyBN1sV2ntLG
TLcRl8WQSIh3j4vhMilEU85rA+q4TuqrOlZtKPTPNGeACwrD7qQkWihsEAKWMdQJ
e++9+CdigL/S3IhMmdTwHHNht31oYl1vAqbQbCEzAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQAttszf/gjwRvkxZs8Iq474
aoBzfsF/NKCKBNRoTdVwQc6DycJylA9JL45BFhc39tka00ttcKGbXmbnOzltnFsH
QuD/1B4pQOESZzUEcsHHCn7tKxIrCn4wk9OiiqcIwHwavFy+guHFSw71jVFhv6im
ILe/K+wzpgc+pUeYiQlWRSuoR7YABZekL8bjpCpuq1kXzP4bV9pnq0sMayCHdH+q
enRnvo4u6PtMUGdX+bye3sp609uFgH53v06ufl3ylkoK5TRuaOj84yYuJDBrAAG6
ZYZaosM/CKXoumetH90Sc2rAvWp2HniHe99STfaw1aNK9YV1T9SjIqhzyzoMzGRP
-----END CERTIFICATE-----
"""

SSL_TEST_FULLNODE_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC792uVfc1mFbJl
uKxzWxZ0r5yaKGjR8azECVrNTcegAjLFQd7+iZS+7DZwEA6Xy/h8T9DZd3Q1m0Rj
lgg73ngO50leCvLqWEvrhueuEIWLdbef4NaX4qkusMI/orYE/ItKgL86HWkGUELn
mf3TkMccohR63vS+Fr6dZDvIw3g+gBPLP9MlK7sdXq1I8CIcV+2du4jhmkA4mJ27
8TdQZOfXnX1hhe1wPuyhJyBN1sV2ntLGTLcRl8WQSIh3j4vhMilEU85rA+q4Tuqr
OlZtKPTPNGeACwrD7qQkWihsEAKWMdQJe++9+CdigL/S3IhMmdTwHHNht31oYl1v
AqbQbCEzAgMBAAECggEAGe13GZfQzVQQ15cxsnfOESpoH5uTWeJMQn5H2Cnyb0/e
UPdVGyc/LVbH641LdgTcsckQte6USRCxzkrTt+5oASZGKIK6Hzkuv75MFuaQhTwn
qBYLg8fwLlCTetOm5+kuDYjU199WrVhE4k2LhbNiw8BXstsuR0o74NoCpR7RZ01m
mHwWGuD9aGMYLlUBqNGB9UztxudbhKOtDPOWqhUHcZA9YuBSEegGPrJEwEo/sP3q
H6ipRmmufX2KUR5qgNW8MzHVSqPns8YJnyRzXrp1y1a9JXEsrBtq7bQcsBkJlZDK
WE66CTewQhx4SGSI/3ktg18BkAeJTUCp+l4+ApIBgQKBgQDy6+qRfB6O4UQwYlaj
8lQf+kRNzjbSBq3BUPbbYthgV42GTcLqT8SIdr+ITy/2ModO/vGaUbrJsGSW4Max
ora+eDMqlz3ucJh+DeYWNLcI3+V5kMzBQNcGPVeAWFgz3ItWiPBUmXc+QDgH9Zia
fGBKj272gLL0rwd1IxRwJw9CBwKBgQDGFhT048DRWYpjCKlZ+lmWKvkuu8uTAl1y
YBXlSEpVeQxev4z0HJFEtiuv77pLGKmM6M5mLW3WEHv2nG1zaYUEJP2C2ds29yAR
2TFKjTxT+6PfFynWgJkA31W7cOTX06LeNRMECUTVX4t7dvSY+H0jK0+Ok7vGNay2
mLlqvqhsdQKBgAfTH5AmHlnd2bNxR3cqdBk/l3mmHc/wFSK39+ujKHMZ/t4HnTKs
9RisMokye8oDYKZjweaFoW2jt+nAPcY1BovmFUfW7VDD4bWVvwaSFh88Dwk2Z9IF
w6dYzHu+3MB25yoXaR5gfx3LNcLT32GChhuAuUNJa/pDtQrJ4XunVm97AoGAKdZs
IrUf+peg5P3lVv3Lgi4dZ0N+4dP0DL5CoaS9HoRsmm52xPBrtkmLvKMzg7z3wq1B
Os+JjVb598JeU6wLzi5J5SNCa7+SZHKtOIPQJCTYHbx0t7t9lXOWVfqoOvWWRryL
AaU7hp2hhjg/vTdupsj1CrYlSN35Vq+3KdaPGCkCgYAtdziasAmXhyR+yjY45ejR
Qdi47tcJU7cuXlvMZltqJG4JgbqKWbbApF8WethF30q2+sDXTQvFNN6l2jS1NVx0
BZjtJMmkEjJxQ3vY4xA4IjdVZJORKkkcaOlYGokNy55SFR7zHn/+qwy1ckWBdzZl
6s4N6Y5uv5tFPWcFgyJlAg==
-----END PRIVATE KEY-----
"""

SSL_TEST_FULLNODE_PUBLIC_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUF2mq+KA3KYyp6bso3F79MnD6AacwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQC5wiF41CixaxHM2oHf3nYkuGmLeG6xBdSogQuaSMAw6KCy
AvCfLDBRgfbvWjXV5teUv61+xgyLctNLmJQBg0owYQhhZnwIZK2jK9h5CvquI9UC
xAdgtvKc6yFKlWS435xSt+ja2w5eHsE0QE6U9SL9qm7OnehvF0baDA7CjQNKQ8SR
lkrl0+mQZCEc5lfroYlpOJ1XKrmLhfX4KV+RcNEuLF4roY1TdkUfCOk9Jq8/DrCD
rAOuFaU/GShqmG9REt3HKIGBO254/xoTcSkGIOHOGI/2uZI0MVUDK8tNDwAaDLcg
RAclaoGQ1++jcjnmjvopsqySEJwJrDJMkpqKd0SzAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQCImPY2TwUGre7AM6nzBqrh
WCXTEct84E1jfJtgWZ5xYdVMNd0Ujg6A89LZnc//KW1xVDImmTrsxwHj/vR7lRdr
L7ADGbKOepqKMgUdT8Im67jpMen9Bnrx/q5dtW8qmUMc+EpGwvMOASYEa5jxQ1Uy
Bxpyk3lpeZs5HZJPG0WVFQnNXtlG8LMlmlj1JAEB79hbK7PqPvat6rnS6NTCHGtC
vjAd8mHjVQJkla6u4dV4oI+niEJk12d1yJ9dMSZ8hO3CiBJBieZJ2v2S04N8UUMh
PQEX/yYT94hLaYWYextZRDxNWnjS68Ju1xv8j8GKdMLE693Z6K5kJkspBy0sEtxk
-----END CERTIFICATE-----
"""

SSL_TEST_FULLNODE_PUBLIC_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC5wiF41CixaxHM
2oHf3nYkuGmLeG6xBdSogQuaSMAw6KCyAvCfLDBRgfbvWjXV5teUv61+xgyLctNL
mJQBg0owYQhhZnwIZK2jK9h5CvquI9UCxAdgtvKc6yFKlWS435xSt+ja2w5eHsE0
QE6U9SL9qm7OnehvF0baDA7CjQNKQ8SRlkrl0+mQZCEc5lfroYlpOJ1XKrmLhfX4
KV+RcNEuLF4roY1TdkUfCOk9Jq8/DrCDrAOuFaU/GShqmG9REt3HKIGBO254/xoT
cSkGIOHOGI/2uZI0MVUDK8tNDwAaDLcgRAclaoGQ1++jcjnmjvopsqySEJwJrDJM
kpqKd0SzAgMBAAECggEABavwu7C2oVwkif2t83jmYI6k4lZGAu+ro411HjvUamnf
5i+Cy0ldHE/8iyhU9nf64xbLJFDFt0hFPUymUDmC/WEpEVhAtzzjtFS1YlS8fK6p
ZVE47HIJjFL9jDptfduN+VSWLoB7utHzkjXYcGHftKEMixB1NVcfma6+kKAflpfX
yA41RixC37ENue4NbUJ2XowVgI0I7MvVbmTqRxx6MbZoO803h/0Vl229+3ixAWnr
UsbEKVkaaX3OUW45q/90nHd5dTjtnwNUAPA4ma1cl6d3sDb248XLKhDji4TQXVIb
R3M2aavGsPf1z3TDcFO/IayKWaOSvV2JGS+NEeXicQKBgQDioeYcmUDQuK7rP1aD
7+fpnv46dkB9Oq8JRrI+EPmUq7xZYLouwjfubYCGSRERpUda771KW17hzkDey0fh
4SRIpJZJ5/lrF2VhlzZJPdQ04UDMyQ+V7YCRkBhZnteQHOm0mHO2AGJBQEkutDVK
5drK+eumCoghiR64q5Fhzz3NawKBgQDR1E+sx3Pf6seUaY1aBTTfwbnuoaVYWvo0
sSpIhNjP/tenX2E/9t+4Pjg++eIf03zH/doiWA2ppktTkjIXMh9gTrK4+xRcLSc3
PFxz0UKIt50ft37bjuMM5xttBc6LelNrwCuuTAdPMBtBdPxW4A5yz5yMMxrqtb0i
y8e+4Piv2QKBgCoM4CVuShhwLAR6PBM+8Ejot0MhrdWOjeuqsmfRvn1XYBs1V1ZV
swsKRk6kQAaGJDc7RGQHkBNVsbOlBDFlFNZls30DDcRREv6IkAoG7tjg8qUMqVeo
ObLIibwXPOgAdVyM7OtYJuL0ip+f0EOVYoNG2/JzAc83Ifwh2VfMnCsBAoGAeKsp
WsqlJ7uEJSSChqeB3cAyJjrNtL81LsJH98Z2TT9YU8e1TKyzwef+PrFDylu8YeLp
5GBREyQwI5Jqvg40HxWDEIBMGCpbaBeNb4mDQs6dTJUhHjDRACWUDyGMw4eIm+m6
9RSCC5c1xXH6gBeAF6Svea0WKK51Y6Jfb7U/LxkCgYEAo8BzWfRRu902NAeWXGb0
SGiTeFxW8llFEG1xfK0pbCXcUjr8jnT9cDLw9ojiBvKyI+AyX7NNT2YhkYjHIwc3
Lq+vn/eD5lx41p0CwhCclAtMwz3lY/+cpxBewC5LBMW+IjYsHELtJyelzwke6DM/
priiJGzzKpJ8pdgZyTyNoB8=
-----END PRIVATE KEY-----
"""

SSL_TEST_WALLET_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIURlqEdkPWX2ld1ZkYRM10UTM191wwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDKHNdtHZzYGVJlTaAmiJDMsNdVpyo3sHewUF23K2zMTUZh
2DBX1heO09RpOIoGIdsgm2P2T/+731O6Hi1+pJyLBq/7LtoPX5fZL/AT1uQN5yDF
xBUvmaFmnapEyRC2tg6H/YNBCTrHO3OKWzF5Zn5dZDmS8D5FcnhPups13k6YYklZ
ZewRTTUxUlnorKdDh2Ur5UPHnpxfG+yRYow/prs6sfQNj1Hdv4nsjEwTPwJQVIC7
xViZMiSWUaYMx0giJe1wggkuVYTBQ6tYCOtbO/FKErYS+NrZ5lUfUzmpzlXIM1bn
Ux+4SwMYddcbedVywMap7mzupD8ZQNCuio9Z7nc1AgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQBghZflsoqx/js1oQC2JfNc
gD5HWNqlS6JbupJr2zt7KaKFVQfXmMEUNcVsEr9PXIGA3vqDnpT3L7Ybk0R9knYP
yGb1c5uRFn5A7moAcJjgwUrDE9GQBx59KRXmK4DofcwinUPEe6BU8sn9VfqjTprQ
WFFLyt941YCxaCCGPgZTyGbHWK2pTQY0aBSQAyNppk+dsca6l2HkelkmUrS6I30p
r4nhJq+eXmehrtn8+zXT6qxmr/vw+F7cwnYyxLswBMc8ijcmvBbkcSEcFbdP8TMN
A4FFYyh0rIijlKTsoEyvUP7LGBBJv0d3RU30jHPBm4faJ1wWXLm6p3hQEJmLzM0i
-----END CERTIFICATE-----
"""

SSL_TEST_WALLET_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDKHNdtHZzYGVJl
TaAmiJDMsNdVpyo3sHewUF23K2zMTUZh2DBX1heO09RpOIoGIdsgm2P2T/+731O6
Hi1+pJyLBq/7LtoPX5fZL/AT1uQN5yDFxBUvmaFmnapEyRC2tg6H/YNBCTrHO3OK
WzF5Zn5dZDmS8D5FcnhPups13k6YYklZZewRTTUxUlnorKdDh2Ur5UPHnpxfG+yR
Yow/prs6sfQNj1Hdv4nsjEwTPwJQVIC7xViZMiSWUaYMx0giJe1wggkuVYTBQ6tY
COtbO/FKErYS+NrZ5lUfUzmpzlXIM1bnUx+4SwMYddcbedVywMap7mzupD8ZQNCu
io9Z7nc1AgMBAAECggEAeIubMUloMrtnmWQjENiDBJK03DFHzM9Dk7VbL9SGn5O3
VsRKkRjwFA/jsJ44NFAdEeWcSVyNetBIb8lv+QjVFVZ3v6jCBklNmAwvdKXGf0RL
F6lLuYg366w90ajafx82q4VYs4F9vTaIQw0BBRdMZwdQD4OaoHEVsPfresWMuvVU
zT43W+PDbRq5gam9Y4VZuFeOBYYEe4mFE2e2CRdKys6w/NsYhbDcYS39OXDnR6FU
1NIYDWN3FSU0cXuwZ8UtViNw7kCMLHvrrW/D7DV4HBYj5KtjFenViAeVolLX+7S8
K9DSQtxzZHL7OmZ6y+LhopWh0pdaftkSwpuq/6liAQKBgQDmlyFpfzzDoWIfzR/M
X6ZwJwOeWLDzeRG0hZETReaEgvmhyda45xumBIWvmQTDzSk8O34hisofHKH99VlX
fefwknZ+M2wcXClnKQgOE7YfYKaReb59PG6APkcgbM/H2rG+eLzGONd9IUIa8q7A
Zr3vlcYvjk/QuxP3SIC6aQ2cCQKBgQDgYl2hGlJ3HENi5O8MeS92WBNhIUDL/ieO
Tsyx+cSxufaX+n/EPHkfacquqX/snbqkcpw4NlxBdpEZo6Lzcr69gCYc8LzN2a4S
CHiGVKonTggRxT6Bp3F4IOH9FwFQ8y+0F7ycOXXkesaL+TUzGx2usvhSfWau+3C9
+Nu9f61kzQKBgQCFL1N4GKqjH+qKDbNJGxIKAy6+3eFOr2X/i4oQxLXxYakHvonM
AIhiqogAtXQgF7ayeHZQr1YxBBu4kGaK90jpFd9k4xSViNHNKNDjOJVfqDZtHhFd
SnNUlSQF4XNdrr4tEpWONDSarIP/Bp7SuEUKRcrTmvIU0IkmsfTQNm9K6QKBgQDa
fQ3cnGvmTaAUQQXAaJRdsR+VubKFsEJGINbTCnmL8Z97l1En/RaYDwRsFOJava+L
B4q0dcJZgCGEDMHUOkwe7BSwo33FGAyWxKbPbsuMoD/dReo6h5hGuAY10lvWviYa
P+7JVG5Gf4Krs4so62N4xA5nDHKbOn0qjpMxr4xglQKBgF5jn3tV5eH2/AyV+CMj
PS9saOsiAZJLRioz/9KB/OIcO/0GH+xBj8nPLXzFuSN1sK6UYbKujvM0NeY5x/kJ
SyB6LZxz++ARJARmmgxKdW8bUxZDfTGrfYyDgWWYbN0SJCJHEDz72XM48lFxB1SB
L4t7t85YfzmrZpeu/vCnqVPT
-----END PRIVATE KEY-----
"""

SSL_TEST_WALLET_PUBLIC_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIULNQ5Bq+zPWOGPtKDkjFf9aHtCBYwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDmIHrbtqy5/pMJq5NZmVRFbX8wHSciOLyUwWY6K6BgOtZH
8WaKoOS03X8KVnWKqXGcUY9DKWar8iQ+VbGP7YLw9wJjr4hNsW1DqN7uzxla3XIF
upT/tKAhZpiqOHKstGEoKwjVD3Dym5xmSP6ERQTfMolo7WaakTpANCGKW0tKM2Rs
6pSaHV4GIvbHSer/apt1zr2IBFQI7Sj9KSXZ1OhOZERSE4FigTAJvW5PEcuVsjwR
LB11vpPKiF7YkLmsj0MQRHlFqZukrSdlvR9ZLaAREJLgk7SwCwUSYGQEGhjiEkH6
vWXT/35IYCkiYNI/vcdCQlN4xBOOAXgO3c1HtikFAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQByHJaF2w67743OsMwKbQ5j
oWAt+rqivYmqJ6tVKEpCAZu3aMPdchcoZdfWRfh/tRP0SwkNE7PwIyRxo0qynrPO
gXhGR17ezrgz3a5AzQ42EXg0xb75QzpkXdrOZK9ynjer4jlMx+a+IJniYlSpyCxc
AnEKvnH22S4j1xCYC9zMDUF6Jqm51h+Pnrz2sHr7NyRu7Lq9cJ62rfyT9kFW/aZX
1/xAwzw2GmyYRpw7ZEiRN9Ipkjs8Nn6yCWOvs/wa6el06mXB/i/IvOdMI7/B3PJS
sOvOjmtIS04kyR2ZB4Qhkty5WSHrF0Se/9WH28L6a6bjFKLRMKLTRLdeZ3ybEOFN
-----END CERTIFICATE-----
"""

SSL_TEST_WALLET_PUBLIC_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDmIHrbtqy5/pMJ
q5NZmVRFbX8wHSciOLyUwWY6K6BgOtZH8WaKoOS03X8KVnWKqXGcUY9DKWar8iQ+
VbGP7YLw9wJjr4hNsW1DqN7uzxla3XIFupT/tKAhZpiqOHKstGEoKwjVD3Dym5xm
SP6ERQTfMolo7WaakTpANCGKW0tKM2Rs6pSaHV4GIvbHSer/apt1zr2IBFQI7Sj9
KSXZ1OhOZERSE4FigTAJvW5PEcuVsjwRLB11vpPKiF7YkLmsj0MQRHlFqZukrSdl
vR9ZLaAREJLgk7SwCwUSYGQEGhjiEkH6vWXT/35IYCkiYNI/vcdCQlN4xBOOAXgO
3c1HtikFAgMBAAECggEBAJNd2U85/AJfc+mNZh7KgZy0Me6tvJG9o4XfE4fMyDbX
dsE7ZV8BCXSJIwGLvFm/iHGCCSwJJyaVOYBxf/ObNW75vx33GmImbMIXMivbk3EM
vifNA/17vc+l072tyEGwgUcnx9AowzuZSt51gAdT63rC8huvazUwKw1SVOg07lHk
wFGsmPGq8O14sytwf1Dpp7p/ixaxyqz+jLLJdrtC97vh0aHzg980IN5eWNCNdETT
TzQ4xYF9jYXk7LzpV/jarfUznre58ohwIEyUwsoFmNzkvYCoVko4REhMF9rHgYCh
XfF+JF8KWAA4Dpy5Dfzm2nXwvEbQhh/xByPFC6G/KgECgYEA9uYvKJqcQlXePuCi
Obp2XmtxhuXOpTqsOsI4Y1JGHQ3VsYE/9Ps4R71uLtqkr/T0k3iybRzguGHIkNqc
J9pFD0NGfQ4pTSmUQtJYa8ndcgCIKh5lKDYjjQDQJKDlIOewVggF0GoWLoTegvAz
dWye1DPdYf07zWTwpatoV2AyCKkCgYEA7pwG/uTWGa9tzaPgIt1x/WGSkMa6/lsI
Eb9w8iDsRlSal94qeQ/7tPI7Mkkm58oThTgY6OQ32T2xig1vtW5uRal07vjKUizO
qjttMj/qLBjw35mkmaLnemhTcWnY9M4nLSBRwMO1o6I5oP6AQXX7kvEL65SicvSD
ptSZL2WlCv0CgYAsYvl7bUBGVLWdzDid9D2vf9VrEQlzfvbToXMNuA7Ozlvqi3f6
DOfzTcTvO3N8Bqepk3tQTm6/9yRdlk+Ygo8DzW5wsQkPzDfRQ4uN5T6gbiQMnmZF
MmZ1xP2meB55Ke3zqYGSFGBkgJKYK6K0q5BqSeC06xfDNzBkOEqL2slj8QKBgCgL
qaTn1QL0jVIg+cIANlxXHtkLcWC0+HK6FYOdgOoA0v0//RLaWt0wdjznSA9Iu+P0
2UFk4/aiwwQvYxspEHrCiOx+dr455OlvFdGEJpIGEY8FYzmhvIWvsqlrIU1ct/h7
3xyh+/8df9yEOhRCb9lmeSCtjmIKpXm/XoI05fElAoGAQcVrN4WoooWchzuhaFlQ
q9T5RDTgooYUi5GDQgqEiPHJJAaqIlAi8kAN82umwBF9al8Kj51JXEEhxJQBMq8D
csxU9ppgBlKPyftgUDwz/agJ6C0zrxAzkNlFzwz0RsqS/38sTjyHiBz3LAjDU8PX
hIarfSKXzCV1ZFJjKvLv/20=
-----END PRIVATE KEY-----
"""

SSL_TEST_FARMER_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUTnXTzqEOILFs1Y6LuvX7UkxgI1EwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDWr7824CNwPS2WHAlYs2QpHVtj+nMn/nl02e3JIX9utKfz
2sVXy9dT0sW7VcDaeUYBi6pDZz8DecwGjvnBMAfh+bkEx9gCs1tY8Iqitgmekoy7
e7+zHJ1zuo0J+p/zeW+Lwg6D0FztarME2gm2tuw1c5FTIfWWnwotYetXxUWCeKNc
+TgeK8WnfUjRcULzyFRAA16n6AmqihfcfVmT/Jyr2eubKeyCJFGUx6jIClb+OFUU
0h4VCZzhHOx/R/X6B9HWJTWgdoKUxQcMt1sdlNuntOkgg1JsJPVPM/+NnijCdHEC
Wsk6MGCiVVH/vtR6ek3sDitsJfk36m5NjiDzeK9dAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQCj7q/5jVqInWNHENfekLWU
u9N+cSMhDMyq/ANc/wm3OcOAYUODAmfgZDuGAmHW73BSeoEuXQdsnxQTCM0bVF5v
9hKcQkLY9v0tez7xcDwicFQfg/SzjCehbeKtKZGnrANLg1tEm2QFUuqmepbhatF1
NREBmX1EtUrZ8l9e0i1oDk13eOJvdkZ5pfQC7UOK2N7dAHQmsWJtJgHpGu9KgdDV
eKRf55N0tiDKFjumdFucvMQVaOtuZX+4bKrLuDE3y6lG/Bzt+ZHZkbCsYAqCtubp
PfGozr3jW+plZvnRz4X2GxQRWFw2jVBcBzu8f8Ahp7q62nT9bEfJ6fsKqwhX/KSx
-----END CERTIFICATE-----
"""

SSL_TEST_FARMER_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDWr7824CNwPS2W
HAlYs2QpHVtj+nMn/nl02e3JIX9utKfz2sVXy9dT0sW7VcDaeUYBi6pDZz8DecwG
jvnBMAfh+bkEx9gCs1tY8Iqitgmekoy7e7+zHJ1zuo0J+p/zeW+Lwg6D0FztarME
2gm2tuw1c5FTIfWWnwotYetXxUWCeKNc+TgeK8WnfUjRcULzyFRAA16n6Amqihfc
fVmT/Jyr2eubKeyCJFGUx6jIClb+OFUU0h4VCZzhHOx/R/X6B9HWJTWgdoKUxQcM
t1sdlNuntOkgg1JsJPVPM/+NnijCdHECWsk6MGCiVVH/vtR6ek3sDitsJfk36m5N
jiDzeK9dAgMBAAECggEAQ59aCIvzPbBXgpfULddbrkOr/MLvsOJMGY1ng9oETLek
y3/Wd0Ai1Clo1Qg+1dIrReNbPx3vUEX2CP7SFpLteLVzHNlh5f/evxYNZREX2JXq
tEdXa7CQu9pAAKur5EIU6521ermP+8yHFPkk5COcJX4AgYIJ3Ga+Cutz+NKPgXew
WIikyHnPui59OZPe+ZzHx2Th1IK6OkzLAeb7EWPs5CbcMZVjmyoX+16+QPY5NqXS
lYeP4R+8No1ZVZr1u4KyPLyHu6s+mUtf6l2J74EhLWwgPlhNGYVCvHPNusO4TuVc
HvJXjt/SyP/7bdL3JWoilQgSouEgWes/asaJUVshIQKBgQD7cCgk5wpe9Zlg4c/g
54XrdC7TJSrvzSyTUjwNRK2jSJ2gk8lkbfdEHX/XWKz4O99AO3z8LlKl80429Et8
Oze4rInxoKmzh3J/gyn3udOmJtGRd9RJzpPVxHodbD13o6bVuoMCCnUdx5YzSkZG
Dnu0+YvMXE73VCHrlO2nSnbDWQKBgQDalORBhTOg6BsmFACRifMZI/hxpiy3SVSr
+t8Uhi8vp56OgtyqjCy3SJfS098Pjb3AlxU/jn8kY3bJDPxCs9ty1+WxQI9VDcTn
bWh6bkUs1ywqv3ujHPLUcXU9aMdfrGFnr/u19Vdo/ZwIB4AooJW+mHe8MjtLN9Tx
6TQMrc0fpQKBgQDkpR0cUa0wpQ4Q98ddsawqbMCX6VieMGm0njdVqXps3X/Zogql
dQpBusGiRlUkdu2RL4d8m3M0zYf2mTh7hC4rlVrrizpGs4j/Q3tKdoVstigkrF8z
rtLotX6GewN6ZCs2eCDiHjhaGEER6xz0X/9Glxb1g4ubhbpCzG9AjYpqIQKBgDfc
p30rOqebyhxwLjkDxXIeZEc/TdxFzHLreYm4RWTrdLU9MoIPsvngfpSt+yrxcZY/
xnloxIubM+dr/yhY6POvw48KTddR3om6x2HKvrkYALyoFUP5iQHMQUdBePq1hmtG
aZD2M7GsZu0SZal8aOi99JPPTqIJkc2FaPz4ihzVAoGBANMDz8fD3OkbzQxjl7nU
AcX1qY05gZrv86SEMECz5TTONBwXU7QiUwp6ihC6FJ/pFfT8MjYmBKzhh/0bHeO8
IZbjDgsZM3e96LJB4uhyps2UaKNrP5Hptw/M58YbSzW92r+2FBucF6vH2yOjIT1E
h46Z/ZztK/e+f65ANNHtAilU
-----END PRIVATE KEY-----
"""

SSL_TEST_FARMER_PUBLIC_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUR24x4LgpE1t6Nmpk9Lbcm2p9bZ8wDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQC2ye4u+jn4ldMnKFJTrpndM/mgaOI9irWCQ9/kES44RvYz
SCWgNIqU83XC7siCkDTAfmQ5dPDgwExGp9mqbBjLa3QuWLiBSmstk/RdvWyYTyv7
Tk3BXjmYU6nbBr0p310+D5Jw8RKB7O88wM603E5Cb48GKmh71DY5+JxwaIJbFATs
DmPXQ5tIO+z2WZmzB/Zba7pYOILk1XDR4YPLgVdvOGlaMCkfMALYKtdW9ek6hIFS
oPlm/mbzbIld80PYP9E3Sf9iX55GVytuIt5B0u6PbUYFcrKyNld9K1UEA9fyNECa
KUVe6UK1Kc+LYGdkRv/qAmMG85zMM4CHs1dP2jRFAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQAREhwgP+CXusazRom0cMeb
KfKZIY2TMHWTYceAB21vUDSor8dfDNZNaJGqNDWJiwxMdqCa6k5u4ClBts2silfs
qYWGQvUpygD9dq9Nazsf8GATZJ/X5OfVKSb/j9OsmikirngsB3KfoOVUz77aALec
yuH9tji46NtYUXEMYsCvQ+8SAmLQNra/jqzM/SHAL1Rz2JNxXY2ldBpsWuwaau8n
j4FqvQtT97zC/RV32B/Io4/LJnD2bvPd41Wf5YutTOJXUFuVDQPD9rI0VkZk87a3
o7oGLlusWLZ1ZIqTylCNVtv/Lz0JXwImhYIsDcNswVhNIWiKHSJkR4aS3gqVt4Sr
-----END CERTIFICATE-----
"""

SSL_TEST_FARMER_PUBLIC_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2ye4u+jn4ldMn
KFJTrpndM/mgaOI9irWCQ9/kES44RvYzSCWgNIqU83XC7siCkDTAfmQ5dPDgwExG
p9mqbBjLa3QuWLiBSmstk/RdvWyYTyv7Tk3BXjmYU6nbBr0p310+D5Jw8RKB7O88
wM603E5Cb48GKmh71DY5+JxwaIJbFATsDmPXQ5tIO+z2WZmzB/Zba7pYOILk1XDR
4YPLgVdvOGlaMCkfMALYKtdW9ek6hIFSoPlm/mbzbIld80PYP9E3Sf9iX55GVytu
It5B0u6PbUYFcrKyNld9K1UEA9fyNECaKUVe6UK1Kc+LYGdkRv/qAmMG85zMM4CH
s1dP2jRFAgMBAAECggEAe7/QGkvcDXjZoGwC+JZ/oqt6d+gqKwIKimuLW2tqQD2C
lwtkNcb8f4UoF9XzN7mLjTrEfcW3AmIOAdPHYEKYsrdHy8zS9O0+DHhbe08wAxmu
rA/CQoSZN5CEsT0pufx3svl16jK7leyjtxzNlNKFxSKj0MfLPvJX1/2BY/TNM/z+
pgiVZNLqVpKwEqVx6awyZKSWimP5pHRJuSXyoXauXLBzj33j5mYP9MRAxIn8GE99
SRCoJB2g6Pa08g4+1cWpyS9mR+9gLilYkuXrUZfG/Xz7L5AHm4w5RxNDu+8tU/Bt
9d3tNLVuFSI4VInD9/GYy046gYM6KvGd8sPy8F5VQQKBgQDsFVSZPfl0ani0S+++
X9FQm2YF2PSmuAw6Np07kNfRluo1hYVqS7Cn1fjnobVPeWBGpGnlh10mkIVJgfxi
cqg5ILNnzSMhRuMNb/SacRJkJvl7xNfKPZ1PGpmk6tWS4T4Np2fY7+IRE7P+gFc3
9Ckbnwaqm2wO5In4/c6NVbVOdQKBgQDGNZpX81wxapjrVMlpsDLnCUaUXvxiN2E2
NLRrW+rg2BBw7uTT4l3QSsuQylM3UHW35jAxbYEzPUTnwAUpTMd39/p54kbMWMRX
hyKvBWI0+R/Rfv+YgYABH/oNktrL8jFbd8LyRZ7RyooWxcBrZMC2CvSruOL9doGa
ZGKGqjU0kQKBgQDZ3dV0lfzfsmIyAOH+je5ctQwx2UXtlWuzTTNNBR4mDV+WhOHa
dn9QY+aP3Gu2LAztJE2VxJXyQOzAKXUAZU9ZaRQndug0jXZ7sBXLcQ3H3y/dSIrb
2ICTv7iKuSzfn33km9j6GmZF3Cj/dPEIcgp9swQz7bqLA91QKumzBKWNAQKBgFkx
/gbeKPrD8ZTVTt4UwJNfhTd3lzPLoB94kEhP0N7l3GA14RvInlcBkaHSqqgVuSPM
nptfn+ijBcMUkj4HoyvFmB4JSbrjp1eMJHuGfK9B/KOV9wd2H1hiP3CkSXnFv5hd
yIil89aMwp+E1hZ9/IrvWzN7vAo7rg8AZaYcKl1BAoGBAJ+2BDW2l4uGOIDc8KRh
SmPRecSs/T4VaEurSkSTCxUp+mvGgw79+hgq7f9dW1Fq3TDr8J1CmY36mT08MWV7
+ucP16bGqR6jymQPEijtthKvnAXihX1zfqNNOn9IUx8zSsyS6gx40za5VeugJc4T
FJsyYFxZ+2EXCgIm/y04IYuH
-----END PRIVATE KEY-----
"""

SSL_TEST_HARVESTER_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUQsRmXdBM+Yt81O+qtGzJpULDwhcwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDc2huslrMBGoEROWCsfrd4LwHPSXrehqP8uthUzpsxhxJP
HU2bDi4Q56IiAaXl33txbDnKE7zOE205rp0h/k3mvnbo9zBFHZakIZuySP5L/+ry
+Jyld9QuggpD5mWWHW6lCmUtGfY0UJJJbr6KPyMqzzQ0xrjLAPWqVvNR19Iapd5D
GsWgBSpKyUIwPUf8JpkFvSv4udZlrONoMA+/PAVEeCgOKbWdwi8vrpR43VcUPSe0
TbxE/bWHgOSDW1FtE46logzJLOzvx/k3Lhvumfrr+znNsZyjk14peqkdAUtOA0dm
VEhs/wHthVkw/47MO7G96DzB0NI0++anRhNXLiAZAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQAVNEaquHBV5LaHJDGrr66p
xPuM9sjaahXr01VfAFBqFGzr+8ZH2T7VL0bg0vO3aimM+Kp45eRGM+gffZ70ab0q
94CVT++3rhoro6nXhx1U1lHRNRqVOyGImwMbz/MtmIAeme7My+kZDcNlFg+MC5DY
0pjN/EAoBslrhGp7yWzEh6oo6cKsYajfqcrewwMRrY7shqrpH/fs9gAB4uzryCVV
54tBj69C9JVi0d06YijpLcUT5czScd6yPlX61XKR9lpKUDyEGbRU+4f4DP2oJzzq
6tsME2HXXcZr2fsxkBeCjZpDEsKPMxsHBnebwSTNESCLQgdQc7wJ8QVzgOkAGoNg
-----END CERTIFICATE-----
"""

SSL_TEST_HARVESTER_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDc2huslrMBGoER
OWCsfrd4LwHPSXrehqP8uthUzpsxhxJPHU2bDi4Q56IiAaXl33txbDnKE7zOE205
rp0h/k3mvnbo9zBFHZakIZuySP5L/+ry+Jyld9QuggpD5mWWHW6lCmUtGfY0UJJJ
br6KPyMqzzQ0xrjLAPWqVvNR19Iapd5DGsWgBSpKyUIwPUf8JpkFvSv4udZlrONo
MA+/PAVEeCgOKbWdwi8vrpR43VcUPSe0TbxE/bWHgOSDW1FtE46logzJLOzvx/k3
Lhvumfrr+znNsZyjk14peqkdAUtOA0dmVEhs/wHthVkw/47MO7G96DzB0NI0++an
RhNXLiAZAgMBAAECggEARghr6ijHjrwG3Z1iSJDOQTA21LKqYdI0QjpFy27Qy73X
UnsqVtcCSJ4LTdlT8DcT//2fvbLQllCWvEngzhzEOz1+m5V3GxOs51M4+ionaZY3
vOCVW+tJv43BD5MJ97ZRlchcGRc4eZJrMRoLFe+7iSG3nly90LH3NRLpibR0jbog
YHJuavvPA6cKDsrPhZN87YkHbrmYu78HrBVX5blws96HxsMqXRlrj6/hdd3MyZSW
IGbIbLKFP5Vy6pBbAXCnY6uw8oC2HvdLis2nEx3UOs7Ktm0AyCR1/OQ1MnLugVbn
iezo7Eb2n+n+3k3X0cIv+SlQZwGgZRAWFdtjGsvL+QKBgQD7FBE1UlNAiqgrS0IS
/l0jLOIPRl/OwMOFzn6oVX7u4qx93JGEsZEYE/0l9DthzRTVbaiat5QZFLBXFTpi
moxBBLu0RBCGJCnfIe4/jmZUobbSqoXMwMbN4AKRM5IjKHQEyRo36fGRLg+eqVFq
pSzK4FGyiah/rLzuDzpwQut5gwKBgQDhLly5/vpYU6DogXAz7V3Q/YQPBr6N5c69
kj19DjivPJQ2Qxl+y8XDv6HyGxkeKGsqFNGEJ6a8RyAMh+IKawJgxGmgjiglRAY8
J4PiYK7wj9pyQhf9QKybs6ahjI1f0oQ8ngJ5QKhxhoRNzfXCM7JeofOMgbKdl318
IUdFSPJ5MwKBgQCi95F71KWo3Nbu0vheL6/wZu+MDpedMU03iqJ3TJcJIyPmxcXG
JSMSR9cmTXJFtsFxDq5DTijYZq9WtragzcN/aD0VcqBvEQYEiJeFtT4CbLyn3Hrg
PbhMZLwF1z1hiJ5VhNp5tGVRYF5PE4N+/xsly5f7lJJD3LD8q/G4cBc7VQKBgQCO
EbYnExvXhkvK5X9pA6VhKdGbuWGYHRlmuVFaCRLyXIIWCheXy/CmI82E9lvOjymt
jxzxCCNGPomV3lVaxVDmxITv60Cg4l4crcGjneRBmkD0PYbtHVTJl3rWCdtYTXVo
2TguUAD2PyxR+lPHht5OnlcOmvWaP+3H1yckK3XvyQKBgQC21g8EqK3PhRUBV8U1
0mTrw39O7DcqhkfTqXRMLLViCh/RLYZmkT2JY1U2Kej0nD4CNBYrQWApRW6srp+I
FOW+1kdmTvaclFMal4gbBraRlt4veqf2dCZuxQTTt3SCf7Rm12jmIjyEH7LfFM3W
2riEhrrEJcofPkOfK2qSifaH9A==
-----END PRIVATE KEY-----
"""

SSL_TEST_TIMELORD_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUXa72z76zyiyFs6cTa7GIU/m41T0wDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDTSy0YIggCwTF96eLR2AxXmpXg30F1eG4SZzr6xWd5sXiL
crUjSc6V9YZRPF+g6ODEryNYjSxWlYf0EtFPD1MGLW+7ssUJrWK1BX+FFCLvjQX6
ShfRFoOqmkAhWp813xYaWihdLLv2UglphfekREFhRw5h8ikfk5JA3AgTFVGFjB/q
1pZ7gWVamhjjzvrbhiXdqcHDqMuNUMQoCuPLlMOq1D59nzYhUUYZOTP8aAOD2dj8
a8plM6OQwAuQarqt9DW69Tm7AxKbFrXnzXqTT4Ccp4rEJxscV8OIP2DVioFLV37B
EWq3pVcarIJku+Lxcpf4C7jXvhBUYAFVeQLMmjzXAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQCSc1CA9sp1CEbEV+7+8EOc
5v3DU1rTEW4dG94MiWDXH/s8B+nWb2lsXLd9Gmau8S+/c3c8rW3eejS7YZ5w7lnb
NOdc8SUwPDM+/f89UCiEeuk9fUIe9EK3pER60Fn4H/0ZXQhVob+1lGScnIyx5vr0
Hq5rPO99qnZ3kgLeYRfHQygSpFQ28XHOkQGVSklgCbCBdE0lNWKpaw8oxw+Ki2zb
tSGF5Uoel75Y3e2ZqtonZCuvE9Q02LGmDmmfSrRuS9jW2hvV/CHpRnv02GMPQT4+
JTKtqOeY6+hI/eg4UKBYbGLY2Sn1irKMRFwAzftgB2eeU+Bhxb4ioksFlhDvzkMf
-----END CERTIFICATE-----
"""

SSL_TEST_TIMELORD_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDTSy0YIggCwTF9
6eLR2AxXmpXg30F1eG4SZzr6xWd5sXiLcrUjSc6V9YZRPF+g6ODEryNYjSxWlYf0
EtFPD1MGLW+7ssUJrWK1BX+FFCLvjQX6ShfRFoOqmkAhWp813xYaWihdLLv2Uglp
hfekREFhRw5h8ikfk5JA3AgTFVGFjB/q1pZ7gWVamhjjzvrbhiXdqcHDqMuNUMQo
CuPLlMOq1D59nzYhUUYZOTP8aAOD2dj8a8plM6OQwAuQarqt9DW69Tm7AxKbFrXn
zXqTT4Ccp4rEJxscV8OIP2DVioFLV37BEWq3pVcarIJku+Lxcpf4C7jXvhBUYAFV
eQLMmjzXAgMBAAECggEBAIrRPCo7yYmNxedUr0lwqQMxM8EOzKHR4ndCzTQOV6JT
H8B2N12c0xYgvgNHKAi+l1WBPzahYXztNun7JvrLNZ+8YEkv9VYbTNtjZllXVnCN
9VxwK1+abBy8xN9k+27YR1w+2YAFsOPvF/H1KzMICPBRT7i38Z6mRJNKPB/VhL64
lGbwmYRUl3KxGjanfiGmzRRARBJA2lIQ+wCUbdpi1HSyktBRdegMYHEn+YcWNXya
WZib1tWF8B2MtJppjjP57rQuCJNRUCnIu44ybw4/zpojErtXLhT6iSDRmXMvfGCx
eJF4J8sNHgFpNtdhLzTCwiD+2oHWygvPNI6oawxcwjECgYEA7Ge51RJeC/5tug90
DxzF+9l8k1zbf+4FcsK2cQwdAJiiTSMaujyj8uyX0eQ9HJfQNBcJo7A7cKQRfHaL
cnw0qNMm7Iu99V5+pyWkZLF7Crz43T0iez3DE6jD/eclwM8mtt2Bk/jxwioWV41u
YX8Kaw8V/kdZvqPm1MWEVZzBHz8CgYEA5M6cEOpvweNZcE4a5+K0QbWRTCNuxlD3
Cd9up2W6CeLVC6tjVfsmVsAb1DI5CYteeAro1BWoiS+7RpZ2IVq+DdRRVpOdWaAq
aaY76ekK8mYdS/CQpBoOltJwXh3XAt9pZ7ymRqhpdSO5NAwX+U+HvEEM0w/Pdy9K
qM75MOOslGkCgYEA3+uv/b6UDlBEpsQUbmwWq+LpOLvvvVE7H+SG4rVSk0oAEYh6
vITL1kF73HeP2xGBSJW5r64x3xPI7Fds5lf3mSHH8K68kzmaRcBF4oqpvRYZs5VA
n/N0X56vZkQXYnXUecl9/ycB96Pd3bg9IWQv/hAgCOaUfxrIfilIm78KvgkCgYAH
tlMaWtyTe3dLSsarZD/RKy6Pk24rbxU0lvxi1hH0PVoS/57kigebyvPlLiAwCyuO
/kckxuocXaiBU5b9vtJDIxHuyiD2oWhskTbZxoog64I3Sg+GCH7PZJ52/ah+p0sl
PP2Zyhlr4l1evL2eIKkhlku5XYIPsV9h20AY/sOVaQKBgQCWV8x5bl9bAmyKj83w
8NBEhKU3zKHkcD0M9+XfjdzxwYLHkQ2X2ftA6prrEJO1NY90PCdNDygJ/m//3tsY
/ClatjEXGrOV34EhzxQd20EQzCrOm2/DZMOL3RALIVW//vL6LNcuytNSKYIAz76a
5NjJeF+rpn62syvQ/MDPnLE2Yw==
-----END PRIVATE KEY-----
"""

SSL_TEST_TIMELORD_PUBLIC_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUfuygNa26jw3yA1o8IQkLYCW31D8wDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDlsfb6//PmK5sQ+v3l3+IIjiTdRcoIxHB3e+fMu6kZPD0r
xLiIbQtw06CZsX4yVF3DaiIPobGKfI1fv7pxyHM5OldOAn52SFIWjnU5PNGfrw7H
+6Z1yCnB6lC89UO39ArbfiNrYGpf0Lq99ECHd/EjRP/mMd717fOQ//2zkhzeenXC
9jRffLZhkhblPCyFepVBAmBQPKB0rNmnhblwtueUM86LWPq0FrDp0MfP/HbgPQ/v
VxY1Pd0mBQ23xXnKCQDg4buXAqv9IVd/kNxzG7H8+5k2Ji1QSoSi301XWWa66kXu
svWc4125avodKiC5t3Czbce7kLAq8mvU32GacJ+fAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQA5M3qJYfjlVzdXzu/JTmG0
4Mp2G8cjAXcSWEPwz+FI6gImLrA4tZz5MER5WxMQF9ALKKPt58qi3hk1b8Ko8OUa
wq802DBkg+LpurAmPNht3IZ8s4oTkSWOP3b0FYA+/rYqM4+EGBcso6cGSl6msayc
0eyUO+AlWYg+2Bw9AiDEiAiLMaODgmMh6ztmycNluMhP8TNOzQRqFlrEs6YvL/z6
tryToIqZVjIZogcU5Bko8KMcLOEWbLprSzSd4CIJEtuao3TdbU40TZmhUgcorX0h
GKaAgtGOxcYjApuavtzr3BA1X/HKLOUNOMDo/27lFPSL2PhSBBRZGGU56FQm2LB4
-----END CERTIFICATE-----
"""

SSL_TEST_TIMELORD_PUBLIC_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDlsfb6//PmK5sQ
+v3l3+IIjiTdRcoIxHB3e+fMu6kZPD0rxLiIbQtw06CZsX4yVF3DaiIPobGKfI1f
v7pxyHM5OldOAn52SFIWjnU5PNGfrw7H+6Z1yCnB6lC89UO39ArbfiNrYGpf0Lq9
9ECHd/EjRP/mMd717fOQ//2zkhzeenXC9jRffLZhkhblPCyFepVBAmBQPKB0rNmn
hblwtueUM86LWPq0FrDp0MfP/HbgPQ/vVxY1Pd0mBQ23xXnKCQDg4buXAqv9IVd/
kNxzG7H8+5k2Ji1QSoSi301XWWa66kXusvWc4125avodKiC5t3Czbce7kLAq8mvU
32GacJ+fAgMBAAECggEAYp5YNkgyhb5vI4k//bR0Lcwp078lEUKWLxbJ3UMtRSJx
+RrLR/fZk6WpLJPiZOWIJGCrIx7/RUBYyqVc/YFcx1NfLKUxesNuSzT664pLTk4x
AHfxblx0YUejRp3fZ1mmV7r+phmNUnoh03DNS9yZcdUsMb9zxQ9XJghi+vhe4L3P
BzxDJjodLkUsvZh64NZcwWqHM0dE+4tR5s9wUfEz92gEe4v+E69EmLC5ob/+h35/
+P/a0COmD0DDT4f1LDLONt/xIKHjQHeg0ccLkV9T4XULm9jT2irUcIme425jIrPV
PFQdyboVlBttoVyoxgr27tiz75kKbQ3pEmgkxI/u4QKBgQD5Q7mmYkZqLz1Xb86C
CHEKMkIfLZ5nzwKfeLPYboNT+KymJI6KD6uL0tGagjaz2KnSY0vyhWNcAEeluiHJ
ZOfo80VmrvhU298YXIfXv2dc8lnA2zMu56ACTLjtKOZ9uv8RnA+xpJdY0lXH5zSj
sB8m68M4Lc8O9Ei8KigH5ELByQKBgQDr5t6Rkbwd3bKz+FHNtDbthLRGnS6otYd1
rsfFFVRwgHh5gVWf+RvcuX5YmyU738VkvvB74hatTQ3T2qxctcY3/hOf9bbuR/jQ
XWQhwdpQaaASB1D1+ZwFAgwbGYevU5fwnSgKeMxqq90eTBCCIEBWgC1mvL9yLQi5
EkI/jrlKJwKBgGAzKBozwXNHqgftyahbs6y4utYnmAP+W8fKILa96AdnaNJyN2TH
KXC8O1LDQHNmghwFYJFHs5IVNZGbZWDBhdNc2AMKMiMl/FL9mxvD7hNsIQGSV42Z
rSJWE+TLrTEHE1vrfA8WM6b+/kY5UBKAbXVq9hvfahMealfceTiaer0pAoGAWsE2
LTCw+5h4EK7e4dGMNDKSnHwKIFO+KnM0XckH9EQolS5Bv8q5gmBGkFYXrAI50bl3
kWF4sfFr+W4uU3iHKrFv4WFJoEBGI/tZ83a9w6PvNiBkcE04TeDswVxADB6P3LzJ
U8YHdp5p8ib3TuiTd/PWA6lnycgzi+fPXt5MwI8CgYEAusoZUcey3Pw020LCC2HJ
Gs6yHqyGBJCtDnjnCLoVXJdPQAQz2YjTHoOGgStKvADdYCKRPiGiYpwXyyS6TwgQ
S6t44Es3eaPxiysbwZrl9SYarFIzN/8gErylU+qvJpNUg1GHdiT0QRmLGZ7679hn
gPSjDIJ2mH3IbqiM2oyvqgg=
-----END PRIVATE KEY-----
"""

SSL_TEST_CRAWLER_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUWOfPmS17sBQ2KK+z+yx4bCQgBiswDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyMloYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQD9vVqZL4co41Wj3v05i+zWg7J+9ODBraJDHeEaw3T7fXDD
I+ZmzNDER6uWmEGqFOvXHdwi2b0mDa6+LLOB2ksOiLknMME7rAF1BusxhYLypF7t
8uQXq1aGQ4fb8LN0llRR3EagfB9mQEJtLHksK50Q39tL+00L/Te56zvjwJR4IwME
MifXGQF0TbN5ofVPOxVczpo5cULvVyLst8S7C4qCs9iHxWFe+o7CXlJRtedNL00+
SdqkTllHXeEYM3nmSoj15telQDTW9AJyHQUTB34qEt8o2Oa6nrrEBRNHZGlBmwcF
EJt0EPpp6A4lHd8Iq/aQAhrweud/kWzde9oMBx11AgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQB0VYSPGkkpREqo5NXcXn3h
vhVmZwV+M1ZZac0/P5g/ILxhRSIWn1JTLd0y6eFznEPOYrQHZws33jsfZlU4OyT2
8Ypxp6v2TRZjY4RpEPy85VAqu5JU0+FZpJkHt4PXaLSnOX3Nd1XZi0AXtQHLvrTK
qEe0A4v0hkwAQK1Ds02udRn2eyHSZVfMVchMPJSD2wrlZ5Mz7uIWNu1jdTrNzHsY
sSBZlwrOzUYSgYP9YucbzEquj/tmn2rhZXNDaFZZ4/Rw1kcKH96vBTIxKnf/ocla
bYmP7j1r3Auw6AxLR5zUtybAj2M9tdE1c+qSP5mvN/ckCBhwOP1XuGjHs40bAiea
-----END CERTIFICATE-----
"""

SSL_TEST_CRAWLER_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD9vVqZL4co41Wj
3v05i+zWg7J+9ODBraJDHeEaw3T7fXDDI+ZmzNDER6uWmEGqFOvXHdwi2b0mDa6+
LLOB2ksOiLknMME7rAF1BusxhYLypF7t8uQXq1aGQ4fb8LN0llRR3EagfB9mQEJt
LHksK50Q39tL+00L/Te56zvjwJR4IwMEMifXGQF0TbN5ofVPOxVczpo5cULvVyLs
t8S7C4qCs9iHxWFe+o7CXlJRtedNL00+SdqkTllHXeEYM3nmSoj15telQDTW9AJy
HQUTB34qEt8o2Oa6nrrEBRNHZGlBmwcFEJt0EPpp6A4lHd8Iq/aQAhrweud/kWzd
e9oMBx11AgMBAAECggEAeZwxOc3vp4cdWobbMqN/hWhlOje/KNRBOo2tf5hCDu6W
BtDD8m0jeY8oC+s5PXz9c4JaKVHWN9DC+V6PQiMPag3ZP5E8a48Ku73vJzLoCccB
wGVzMGzr8TmYea8pMy2BiCJcrzoOCoGt1IlGIgddJeNERWxSBvb7qF23vHZmMhUR
ZNt6l8n6ADXL/gYeCue0LkK0OSb66Hdb2swecjx+aelMHudPfYjKdVtDLj/5kd+U
NgygosIiJqa/KTgv+ZKCFgPZgV26guV8Coav8b+UDmDOmevO4+a50iKX//KsR4Ry
KvzGR64ILp1hBT9PwAomH+j2MRzAcDZIFV1cr9Q+AQKBgQD/XY/eGEYRJPmPrWI1
BC1Kvmni9fXajc6/YVIliL+rOoPLPkZTWvkQZh6PiUFC9H4L3yFHhtWMmn6dyI5w
B6O1pr87P5RTyfJ9LpnY1epXRERnIAR4Yuh1W9QgUzbiP+Y0jYHbSQm8C8EDPwnL
159sGmFMD/fwnEEZIsqPxVMZtQKBgQD+XsH7FcAII8Z4XdQJYGCGMHi+y634teLJ
/f1vWfsEJoeJYaiJUoXzrJSVom7wMbEwgPFTmM/SGNLDDwjeoFjYryIB6DIyUfk7
dGykQY0v6YhFUUx2K1QpEdPbBSx/oyQXmiwbEo8DD6cWF5SYux2KfdngH1OAOnuz
TV6MVSNMwQKBgB3w1mFv7ycrcqdJ6O3WY4kT8k5OEFljrw35VyxXcEGfRryZvJ0h
WXp2vraNnT1AdVbm/nvobzlhE99kGG9CNguiVWGY/sckMm5C/H7T9fntYyfENUH4
NtErxx9TImg8nb0jqkoPsjh+GE9NINTpnyOJpEbKyINJjshnr+BTfn7RAoGAG3XZ
VSTU9Uv/ahEfCeAYq4PiFR7h6h6gnBPKX1IEcj9ClIcxbZm2EkdIRxshBNcofMb+
xnqRvOmnHx2pZHdFACdv8WrCuIH2+P8pl1XoSwrYBjuvmHY3ALQG/fcCBclz5QRk
zItlWvw+mnjzNsXEe6X4dmSLXCV0IzgwA9BRHkECgYEA74UZh8R5iZNWjt14TYay
0D33Qhu4nFhRtdqlIMZl6GW7pxqVYZKD512X+G6AVDceJTGmzy94kgc/lb7YtKCw
3nMFPncjRhG98rv+O4CobxjxtRwNTacbwFD+/yYxUCUio14agPezNbX/oEGe8cGL
tsqsAShkZwiJbNvz1q/u6kw=
-----END PRIVATE KEY-----
"""

SSL_TEST_DAEMON_PRIVATE_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIURUSWnNQeBOShv/Sz9MuDq2t6VVwwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyM1oYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDEDI/6MSomdp0AjdEuQgP6og1bMKOb/X0G9mEpvKjyIl+8
SSijACXVRhSG7Nx0tU61pebjXF2ax6jgqpzSrrlv/w6WxSmRcqbrdZFSUWMG5FFc
dYfSKyrMmF/p0o0kXQRaBSeIhkLnGS43Zna1w5b7ak76EttzQd5uiJ6bG7vCpGn0
hXNgdXtRIaruK4TWt740F2vyhIRtsEIUURaLe8MPT8ey4lm4Fz2URnUvfdMma7GS
rZIsT17kw7SQBlaqoGXslYNB2yMdnAWRJzuh6cvnxQax2Mfciwit5fkFQlnVPdZx
W/rLffyCCef9Z0m6WArb76OTwcCq4pmwh3dfOi/ZAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQBu0wa4sLoqzpBt71pELonc
siZZ+dCLuFCXvyt8nQcN8arR7Dd5/eb+kn1AFNRFggbnf/z/jTc6ujISUrHIzAkz
mVbuwzyA3gKzZfyTgv6H8N6qvqLPBTWMgs82UXdKE4gXuheUT9+lAp6z81FbuFK9
PSX+gebb/WwxdEP0w7A4mws6udBnOpPW9i0ArZKNKgWl8RiaVxoJWt74AG/t6HIx
TV2iONXfZJO1k4rJb/jsmOavfXDYeEVrqXJ40f20Ex1wWPGd5Hm/yOrFutF7nvye
mHxa/DuK2vpqPuwcJLYr2FHatClZNiCza6JLeMq1CWgEJ0Io9fte87JuP4ZWi4Q+
-----END CERTIFICATE-----
"""

SSL_TEST_DAEMON_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDEDI/6MSomdp0A
jdEuQgP6og1bMKOb/X0G9mEpvKjyIl+8SSijACXVRhSG7Nx0tU61pebjXF2ax6jg
qpzSrrlv/w6WxSmRcqbrdZFSUWMG5FFcdYfSKyrMmF/p0o0kXQRaBSeIhkLnGS43
Zna1w5b7ak76EttzQd5uiJ6bG7vCpGn0hXNgdXtRIaruK4TWt740F2vyhIRtsEIU
URaLe8MPT8ey4lm4Fz2URnUvfdMma7GSrZIsT17kw7SQBlaqoGXslYNB2yMdnAWR
Jzuh6cvnxQax2Mfciwit5fkFQlnVPdZxW/rLffyCCef9Z0m6WArb76OTwcCq4pmw
h3dfOi/ZAgMBAAECggEAUcbPs9QYOe0WNmnxjHMbB8va+GPEi0fkhCf3hZpdeore
FkMKAVwJa/oMi+93UfNi/qBSPBqGLQ8FoZlpSvR5A3+HzVo2qaYCfIsQ8B5kyTYp
vgCEhCVfd/JDZ9xc5YMrUoV95RPkClPVlGRYNh989ih1AxkkkuIx7zdruVWLL3f7
X/p9P9GvW1pKchk6nSqxiXAqiLljOL3mashfiymmXdAJEpRDSwg4dvsviMjbnIvE
/3jIszp/QXZxXjV+UEjPjL+gSLYwVVGoXV+Ejf/9WlkQSrKo2xIrNSuIl/30R1wV
r9KmQjUafhInB6nWRgFxsknb8vmbWZ60wDghopti1QKBgQD7JhaciR6xhtZGt42n
dbFxKbnLeRVet/WKMLBd4o82kRgtH64LJoZ6hWKF8A7uvf1H6rgNUQLX24870C5B
iGJFaBKQ5MHGPagMpAKjwNAOHMkssLt2stFri5thulf8nBpN/dyeCEbBOAanG6vY
cwfV4YOb/PFJ9ODkLeTiKWOxFwKBgQDH1gKcRaeTMbrSm+NySCFxO8Hk09wFR3D9
RkH6BQ0V+Gl9ds7G8p/tjYWQDC1Ts9APyCNKoKC9IFHSaMhfjAO/6qPhuDi3DRco
er8BvcDjA5bBN+9xrezCuGO6T7IW+fY6BgWv9+XH+MmaokA234ABsz7v15C3Qk55
/VcrzgpcjwKBgQD04CJT5m6C8dGjif0YNm0YxXJermTjwcIrR2XvZKP2tGo6NRVh
0eJ1O/DgXzxwE9cNdBKZCVAYX/+8djNjujL3MY5IsIMvY5ajHJdmSu2RlQeiB4AB
MEF49to9448+woXzXX7qp281ngb+kMBxf1c4d3X3dh1d2uIcGZN94JVPaQKBgQCe
3q84mc+9n72NDk3mXx3nLcDaMOwsbj2PvblaEYXzv4fuLPP7CozGiMp0WJn4f22b
/lrAS68+bGFgS9lwzJl2jA45twGv1YJhtiQAOGEOmZ3Sgqujzsf5jioKxq0owxRT
0NHYsdZGAq4Ud4VhmpHjyCLy/oeYiehl51jUBHwMVQKBgQDU4aOi+FwIrdSyqU3e
0ZWpLd9mJ4UEkzsmtDs0mewfDc15RzeqZCi2tQkSvzratYtrNydtG/L9nxaDDBU4
S9tIWmaKBMtFAzGG/Drs1wKrCCH8DTvuv/70kvx6TwbzPDQvg9KOgKFLATiEzRDG
EWSTA/GNS4G4uZ31e/CscomD6w==
-----END PRIVATE KEY-----
"""

SSL_TEST_INTRODUCER_PUBLIC_CRT = b"""-----BEGIN CERTIFICATE-----
MIIDLDCCAhSgAwIBAgIUPwUT6RFj3c1lZddwvYGkWtbwHzIwDQYJKoZIhvcNAQEL
BQAwRDENMAsGA1UECgwEQ2hpYTEQMA4GA1UEAwwHQ2hpYSBDQTEhMB8GA1UECwwY
T3JnYW5pYyBGYXJtaW5nIERpdmlzaW9uMCAXDTIyMDMyMjEwMjkyM1oYDzIxMDAw
ODAyMDAwMDAwWjBBMQ0wCwYDVQQDDARDaGlhMQ0wCwYDVQQKDARDaGlhMSEwHwYD
VQQLDBhPcmdhbmljIEZhcm1pbmcgRGl2aXNpb24wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDPobMhkfO6/94LcS9llcyUkzxSeRcWOnmtEXgJxwe8biHW
5CWrNu5GMiCFSs6Z9os8M4Xl1s3DvYCfxiG5XaA7SqLX1183QMS/a4zOPbozuVL7
tyLpGx511o6gQrHMPFIqc50SVPeW2gMd/PW9WcYXI2rmMOGMfUhI5kGSZFXIWZzT
DRdIEyFYsMh0vNPuMGhcuWglXD1Wv6LGEoDsvFnmvqzbplxgZeSilvUyEMhxx/gJ
XwhsdXnxwVcdg7DWA1adELbiwx4TrA8ws+r5EOK3uvmemxMhwcjMtKPU3LvafBzK
R5MkMQpxY4RehqO5TiCAsJXMrkLoKkMGCtfW2TBNAgMBAAGjFzAVMBMGA1UdEQQM
MAqCCGNoaWEubmV0MA0GCSqGSIb3DQEBCwUAA4IBAQA466vxCP9fhomcXQolSuIj
speXwl0h7xPZvT+0dk+HVJbr/peTKMlg7szvwbNmjJHijwlHD5oim+GB6+WBiSXS
G9ceIe7bBLoPRizsw6b963u8jvKHPRXux8HNspYw18MV8E4SxMB6Sqtk+i8HWgcU
kSu6wjQurRjBMuZtu7abRn8gGhaRWMbu0TRrJlYRDpI6zQJfo+HWc4Wn8knJ0PGo
BqLKD7kCrTqp9eES6WUKMBJ/xLRdIK516I8gw4mQJxO//Hej0o98bkFihcSZMT0o
y4QKE9FN6TjHYPTllouTn4G8e43PnqYT4K8pium+tIuO61W+4OsgvRnk7ykFJpgj
-----END CERTIFICATE-----
"""

SSL_TEST_INTRODUCER_PUBLIC_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDPobMhkfO6/94L
cS9llcyUkzxSeRcWOnmtEXgJxwe8biHW5CWrNu5GMiCFSs6Z9os8M4Xl1s3DvYCf
xiG5XaA7SqLX1183QMS/a4zOPbozuVL7tyLpGx511o6gQrHMPFIqc50SVPeW2gMd
/PW9WcYXI2rmMOGMfUhI5kGSZFXIWZzTDRdIEyFYsMh0vNPuMGhcuWglXD1Wv6LG
EoDsvFnmvqzbplxgZeSilvUyEMhxx/gJXwhsdXnxwVcdg7DWA1adELbiwx4TrA8w
s+r5EOK3uvmemxMhwcjMtKPU3LvafBzKR5MkMQpxY4RehqO5TiCAsJXMrkLoKkMG
CtfW2TBNAgMBAAECggEAL83qAVOqSya4B+hiYkAwHxEbNV3d2+dQtnEsMwwZEuBE
eEaFCbuW9qB57lZ/5ODnw8+VB4sCSwvpfl/Oye/tgVk4zvsuV/lYkz3+6Ek8Asar
fXr31bXBuJ3SrsFMUFqfDFkcE+luK9Q8HX5tUdBGlHM6HI+qjn8V0nr5I+xn972H
zT2oouCoM/2pfwfWVy/K9Z6/z7rcmZNbEnF3n4nh85nN906ofsPuCpIqVLV/1Bf/
2Z+yLLg+ddneVCbULiXyfW32IdwzsK/WFUAUQuwtZNRVQ+Gf0GBZoipur6hIfNol
9Z7HKzu/1207Sd07u4UqbxPaEcwWHmaTCTON390PXQKBgQD0ntD51zWFpjf4NBcc
NOGESHaIXI4VZWPdXZrs8IsGrLvULEev1dGpVqTCIbpDUGfDP9eaMpRare95eRUS
uZk4AAFT4cgUD1AA7npxNHLJ807k1OKUTfRUTbSt/7MY66nKJ0xd8pLasCN8r1E9
j/jx4qVPyZaPigQhEhq1NRD10wKBgQDZSmJ10xxdM0wMhV72kMYtKWOLGVTcSLNA
+ZFzOUL+0AL9UA+qqvoU8evFYXjmqGlAAhWb7OocbhOWyr0YwjRCOADApGiP8tMk
2x6PE8pbDabvRcLQ3/s6qs4Q100Ga1MDW8Mwi4FTe3e79qkY2gBerYvOL+oDPEXn
DPye9/zNXwKBgHx+34hn+PteDxopGKHoX+X9IyZfRIirI1okK5bvDTKGcsmXB5z7
y0rNp+iNVciwgT6jnU0C9PH5l+lQsGLpRotzpTlVrYhYCrWOqY43zTvusnZPykkE
K5dEPPJZMoM6XR1fRsSBki/ueQEaENSuE1q3qL6ksBW5fkR+fE1BBrK1AoGAHQwl
l2yuWQM3gmD97eYyp+zlgr3TK1OIqwHx4L5h52B1VdmzDnSm08/3Xb6HBAa1czoU
G3ETZtOMSNc3aizkAYotB5Oy6rNiaIXmUugpX/y2OTxRK80Vb6VPwM6XXGlSgpts
v3uWwUs7GWSC/HCAJif7DYg4N1CCY73Hs5ShNe8CgYBrW0knLvima3Ug0oBNwOy3
2cnNnQqpXqn2cVfBbB2Om/6q9zclD3Qu0k11gUsYTMyGnXOLl9J7PhKgDqbnvhSA
s4kJlLBYxfILTZrlMeZGkLMtDxll8cUTKJ5AP6gR7AAbm5y20+xqPaIr1gjdGict
y5AZoW69GqwC41YzBDIO0w==
-----END PRIVATE KEY-----
"""

SSL_TEST_PRIVATE_CA_CERT_AND_KEY_2: Tuple[bytes, bytes] = (SSL_TEST_PRIVATE_CA_CRT, SSL_TEST_PRIVATE_CA_KEY)

SSL_TEST_NODE_CERTS_AND_KEYS_2: Dict[str, Dict[str, Dict[str, bytes]]] = {
    "full_node": {
        "private": {"crt": SSL_TEST_FULLNODE_PRIVATE_CRT, "key": SSL_TEST_FULLNODE_PRIVATE_KEY},
        "public": {"crt": SSL_TEST_FULLNODE_PUBLIC_CRT, "key": SSL_TEST_FULLNODE_PUBLIC_KEY},
    },
    "wallet": {
        "private": {"crt": SSL_TEST_WALLET_PRIVATE_CRT, "key": SSL_TEST_WALLET_PRIVATE_KEY},
        "public": {"crt": SSL_TEST_WALLET_PUBLIC_CRT, "key": SSL_TEST_WALLET_PUBLIC_KEY},
    },
    "farmer": {
        "private": {"crt": SSL_TEST_FARMER_PRIVATE_CRT, "key": SSL_TEST_FARMER_PRIVATE_KEY},
        "public": {"crt": SSL_TEST_FARMER_PUBLIC_CRT, "key": SSL_TEST_FARMER_PUBLIC_KEY},
    },
    "harvester": {
        "private": {"crt": SSL_TEST_HARVESTER_PRIVATE_CRT, "key": SSL_TEST_HARVESTER_PRIVATE_KEY},
    },
    "timelord": {
        "private": {"crt": SSL_TEST_TIMELORD_PRIVATE_CRT, "key": SSL_TEST_TIMELORD_PRIVATE_KEY},
        "public": {"crt": SSL_TEST_TIMELORD_PUBLIC_CRT, "key": SSL_TEST_TIMELORD_PUBLIC_KEY},
    },
    "crawler": {
        "private": {"crt": SSL_TEST_CRAWLER_PRIVATE_CRT, "key": SSL_TEST_CRAWLER_PRIVATE_KEY},
    },
    "daemon": {
        "private": {"crt": SSL_TEST_DAEMON_PRIVATE_CRT, "key": SSL_TEST_DAEMON_PRIVATE_KEY},
    },
    "introducer": {
        "public": {"crt": SSL_TEST_INTRODUCER_PUBLIC_CRT, "key": SSL_TEST_INTRODUCER_PUBLIC_KEY},
    },
}
