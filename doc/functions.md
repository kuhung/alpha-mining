A.1. Functions and Operators

(Below “{ }” stands for a placeholder.  All expressions are case insensitive.)

abs(x), log(x), sign(x) = standard definitions; same for the operators “+”, “-”, “*”, “/”, “>”, “<”,
“==”, “||”, “x ? y : z”

rank(x) = cross-sectional rank

delay(x, d) = value of x d days ago

correlation(x, y, d) = time-serial correlation of x and y for the past d days

covariance(x, y, d) = time-serial covariance of x and y for the past d days

scale(x, a) = rescaled x such that sum(abs(x)) = a (the default is a = 1)

delta(x, d) = today’s value of x minus the value of x d days ago

signedpower(x, a) = x^a

decay_linear(x, d) = weighted moving average over the past d days with linearly decaying
weights d, d – 1, …, 1 (rescaled to sum up to 1)

indneutralize(x, g) = x cross-sectionally neutralized against groups g (subindustries, industries,
sectors, etc.), i.e., x is cross-sectionally demeaned within each group g

ts_{O}(x, d) = operator O applied across the time-series for the past d days; non-integer number
of days d is converted to floor(d)

ts_min(x, d) = time-series min over the past d days

15

ts_max(x, d) = time-series max over the past d days

ts_argmax(x, d) = which day ts_max(x, d) occurred on

ts_argmin(x, d) = which day ts_min(x, d) occurred on

ts_rank(x, d) = time-series rank in the past d days

min(x, d) = ts_min(x, d)

max(x, d) = ts_max(x, d)

sum(x, d) = time-series sum over the past d days

product(x, d) = time-series product over the past d days

stddev(x, d) = moving time-series standard deviation over the past d days

A.2. Input Data

returns = daily close-to-close returns

open, close, high, low, volume = standard definitions for daily price and volume data

vwap = daily volume-weighted average price

cap = market cap

adv{d} = average daily dollar volume for the past d days

IndClass = a generic placeholder for a binary industry classification such as GICS, BICS, NAICS,
SIC, etc., in indneutralize(x, IndClass.level), where level = sector, industry, subindustry, etc.
Multiple IndClass in the same alpha need not correspond to the same industry classification.
