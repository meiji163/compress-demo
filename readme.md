# Show & Tell Compression Demo 
_In which I take you down the lossless compression rabbit hole_ :rabbit: 

## compression 
I'll give a overview of one approach to compression based on Information Theory and explain a few compression algorithms, including Lempel-Ziv and PAQ. I'll also go over some recent compression algorithms based on deep neural networks.

Along the way I'll attempt to answer _curious compression questions_ such as:
- What is the smallest number of bytes you can compress a file to?
- What does compression have to do with Machine Learning?
- Why is there a 500,000€ prize to compress Wikipedia?
- Does compression = AI ? 

## challenge for you :grey_question:

> You MLH fellow, you have quite the brain    
> You fixed all the bugs, and merged into main   
> You coded some tests (which took quite a while)     
> Now can you compress [this 100kB file](https://raw.githubusercontent.com/meiji163/compress-demo/main/compressme.txt)?


Submit in the comments number of bytes and how you did it (smallest wins 🥇 )

```shell
# example
$ curl https://raw.githubusercontent.com/meiji163/compress-demo/main/compressme.txt \
         | gzip > compressme.gz \
          && wc -c compressme.gz
```
