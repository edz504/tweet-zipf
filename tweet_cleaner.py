import re
def remove_sn(t):
    rep = 0
    ats_cleaned = True
    if ('@' in t):
        ats_cleaned = False
    while(not ats_cleaned):
        at_ind_start = t.index('@')
        # the space should really be any non-screen-name-enabled character
        # so if the tweet is "...@Beyonce:blahhh "
        # then we leave blahhh in the string too
        m = re.search(r'\W', t[at_ind_start + 1:])
        if m:
            at_ind_end = at_ind_start + m.start()
        else:
            at_ind_end = at_ind_start + len(t[at_ind_start:])
        t = t[:at_ind_start] + t[at_ind_end + 1:]
        if (not '@' in t):
            ats_cleaned = True
        if (rep > 140):
            print 'Reached' + str(rep) + ' repetitions for the string:'
            print t
            print 'at index ' + rep + 'breaking'
            break
        rep += 1
    return(t)
# now let's remove urls (they're definitely not words)
def remove_urls(t):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', t)
    for url in urls:
        t = re.sub(re.escape(url), '', t)
    return(t)
# now that we have taken care of the screen_names with the @'s, as well as
# the URLs, we can remove all punctuation.  note that this leaves hashtags
# (words that follow the # sign) in the string, because we believe this 
# should count as a word (or words)
def leave_alphanumeric(t):
    return re.sub(r'(?! )(?!-)(?!\')\W', '', t)