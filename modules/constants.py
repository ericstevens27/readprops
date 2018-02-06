SUCCESS = 200
APPROVED = 4
REJECTED = 3
PENDING = 1
CREATIVE = 'creative'
ADVERTISER = 'advertiser'
TOKENLIMIT = 1800

errorcodes = {
    1001: "Authentication error (dsp-token error)",
    1002: "Missing required parameter error",
    1003: "Illegal parameters",
    1004: "File format error",
    1005: "File size error",
    1006: "The file size is incorrect",
    1007: "File get error",
    2001: "Upload failed",
    2002: "Data does not exist",
    2003: "Database error"
}

fields = {
    "expose": ["Number of Impressions", "{:,}", "int"],
    "expose_rate": ["Show Rate", "{:.4%}", "float"],
    "click": ["Number of Clicks", "{:,}", "int"],
    "fee": ["Fee", "{:d}", "int"],
    "ecpm": ["Thousands Impression Price", "{:.4f}", "float"],
    "ctr": ["Click through rate", "{:.4%}", "float"],
    "cpc": ["Average Click Price", "{:.4f}", "float"],
    "request": ["Number of Requests", "{:,}", "int"],
    "response": ["Number of Responses", "{:,}", "int"],
    "price_response_rate": ["Fill Rate", "{:.4%}", "float"],
    "response_rate": ["Request Success Rate", "{:.4%}", "float"],
    "price_response": ["Number of Padding", "{:,}", "int"],
    "bid": ["Number of Auctions (padding minus keywords filtered)", "{:,}", "int"],
    "bid_rate": ["Participation in the bidding", "{:.4%}", "float"],
    "win": ["Number of successful bids", "{:,}", "int"],
    "win_rate": ["Bid win success rate", "{:.4%}", "float"],
    "time_out": ["Number of timeouts", "{:,}", "int"],
    "time_out_rate": ["Timeout Rate", "{:.4%}", "float"],
    "filter_rate": ["Filtration Rate", "{:.4%}", "float"],
    "bid_fail_rate": ["Bid Failure Rate", "{:.4%}", "float"],
    "dsp": ["DPS Name (spacesmobile)", "{}", "str"],
    "date": ["Datetime in Epoch", "{:d}", "int"],
    "date_time": ["Date in YYYYMMDD string format", "{:%Y-%m-%d}", "date"]
}
