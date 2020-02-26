

def aggregateTweets(DirPath, authorsFilter=None, columnsFilter=None, savePath=None):
	"""
		Take the path of a directory containing json files produced with pump.py 
		and aggregate all tweets in a single dataFrame

		DirPath: The directory of the files to aggregate
		authorsFilter: the list of tweeter account to keep in the df, no filter if not mentionned
		columnsFilter: To reduce size if too much data, keep only columns mentionned here if not None
		savePath: the path of the final df, not saved if not mentionned	
	"""
	df = pd.DataFrame(columns=[u'author_handle', u'lang', u'likes', u'main', u'permalink',
	       u'published', u'replied', u'shared_type', u'shares',
	       u'source_followers', u'source_following'])

	if columnsFilter is not None:
		df = df[[columnsFilter]]

	all_files = list(os.listdir(DirPath))

	for i,f in enumerate(all_files):
	    print('Loading files %d/%d : %s\r'%(i+1,len(all_files), f), end="")
	    temp = pd.read_json(os.path.join(DirPath,f), orient="records")

	    if authorsFilter is not None:
	    	temp = temp[temp['author_handle'].isin(authorsFilter)]

	    if columnsFilter is not None:
			df = df[[columnsFilter]]
			
	    df = pd.concat([df, temp])
	        
	print("Done!" + " "*30)

	df['published'] = pd.to_datetime(df['published'], infer_datetime_format=True) 

	if savePath is not None: 
		df.to_csv(savePath, encoding='utf-8', index=False)

	return df


def countByDay(df, col_date):
	"""
		Take a df and count the occurence of rows per day

		df: the df to group by day
		col_date: the column name on which we group per day
	"""
    tweets_per_day = df.published.groupby([df[col_date].dt.year, df[col_date].dt.month, df[col_date].dt.day]).count()
    tweets_per_day.index.names = ['Year', 'Month','Day']
    tweets_per_day = tweets_per_day.reset_index()
    tweets_per_day['date'] = pd.to_datetime(tweets_per_day[['Year', 'Month', 'Day']])
    tweets_per_day = tweets_per_day[['date', 'published']]
    return tweets_per_day




