start the server locally by
```
npm install
npm run dev
```
run db
```
npm run json-server
```


response format for
`/api/submissions/1`

```
{
    "data": {
        "id": "1",
        "problem_statement": "The Hamming distance between two integers is the number of positions at which the corresponding bits are different.\n\nGiven two integers x and y, return the Hamming distance between them.\n\nExample 1:\n\nInput: x = 1, y = 4\nOutput: 2\nExplanation:\n1   (0 0 0 1)\n4   (0 1 0 0)\n   ↑   ↑\nThe above arrows point to positions where the corresponding bits are different.\nExample 2:\n\nInput: x = 3, y = 1\nOutput: 1\n\nConstraints:\n\n0 <= x, y <= 231 - 1",
        "source_code": "class Solution {\\npublic:\\n    int hammingDistance(int x, int y) {\\n        int bit_count = x ^ y ;\\n        return __builtin_popcount(bit_count);\\n    }   \\n};",
        "language": "cpp",
        "difficulty_level": "easy"
    }
}
```

