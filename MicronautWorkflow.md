# Micronaut AWS workflow


1. Create Project
    - either via micronaut launch
    - add aws-lambda, graalvm package aws-custom-runtime
    - or via mn cli 
        ```bash
        mn create-app info.novatec.break-even lang=kotlin --features aws-lambda,graalvm 
        ```
2. Edit ```bootstrap``` file
    - increase Xmxx size to at least 256 in bootstrap file to function properly      
3. run ```deploy.sh``` script
4. upload to aws
    - create serverless function
    - set runtime to ```custom runtime```
    - set the memory usage accordingly
    - set handler
