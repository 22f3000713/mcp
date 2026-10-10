import hashlib

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

EMAIL = "22f3000713@ds.study.iitm.ac.in"

mcp = FastMCP(
    name="exam-challenge-server",
    stateless_http=True,
    json_response=True,
)


@mcp.tool
def solve_challenge() -> str:
    """
    Return the first 16 lowercase hex characters of
    SHA-256('<challenge>:<normalized_email>').
    """
    headers = get_http_headers(include_all=True)

    challenge = headers.get("x-exam-challenge")
    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    text_to_hash = f"{challenge}:{EMAIL}"
    digest = hashlib.sha256(text_to_hash.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)