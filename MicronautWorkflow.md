# Micronaut AWS workflow


- Create Project
    - ```bash 
      mn create-app info.novatec.break-even --lang=kotlin --features aws-lambda,graalvm ```
    - or via micronaut launch
    - add aws-lambda, graalvm package aws-custom-runtime
- Edit bootstrap file
    - increase Xmxx size to at least 256 in bootstrap file to function properly  
- run deploy.sh script
- upload to aws
  - create serverless function
  - set runtime to custom runtime
  - set the memory usage accordingly
