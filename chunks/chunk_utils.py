from typing import List

def chunk_text(text:str,chunk_size:int=500,overlap:int=50)->List[str]:
    words=text.split()
    chunks=[]
    start=0
    while(start<len(words)):
        end=min(len(words),start+chunk_size)
        chunk=" ".join(words[start:end])
        chunks.append(chunk)
        start=max(0,end-overlap)
    return chunks

