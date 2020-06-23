## File Breakdown
| File | Usage |
|--|--|
| 1) ColTransposeBrute | More simple single process brute force |
| 2) **ColTransposeBruteMulti** | Brute force with multithread support, you'll probably want this one |
| 3) ColTransposeEncDec | Only contains an encrypt and decrypt function  |
| 4) bigramfreq | Needed for any of the brute force files  |

User inputs can be found at the top of each file. Keys of length 9 can be fully brute forced in about 2 minutes with 8 threads

## Implementation notes
Encryption was done by writing the plaintext horizontally and reading vertically while decryption wrote vertically and read horizontally. The numerical keys start at 0 within the program but are printed in the more common format of starting at 1. If there are repeated letters in the key then ordering is done by a first come first served format.

## Dependancies

 - numpy
