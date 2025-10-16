import pinecone

pinecone.init(api_key="pcsk_45zhZk_78ka5aUitmhiPYpiYVSgrMcQXfjSRyuwR5XVsE8sz3QwQ9o4FPSZNbbV62a71zy")


## Create or connect to index

index_name = "support_docs"
index = pinecone.Index(index_name)