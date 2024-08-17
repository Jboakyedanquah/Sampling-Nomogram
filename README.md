# Sampling-Nomogram
This is a Python script that plots a sampling protocol nomogram according to Pierre Gy's theory.

The data is provided via a .csv file like the example below. Each line represents a step in the protocol. It is important that the header matches the example exactly:

* ml: lot mass;
* ms: sample mass;
* d: sample top size;
* k: sampling constant;

```
ml,ms,d,k
5728,5728,5,37.24
5728,5728,0.6350,104.52
5728,1432,0.6350,104.52
1432,1432,0.2,186.24
1432,300,0.2,186.24
300,300,0.0160,266666.66
300,50,0.0160,266666.66
```

Run the app by opening Nomogram and uploading the csv file

An image will be saved as 'nomogram' by default in the same directory as the app.

You also haave the option to save it to preffered name
