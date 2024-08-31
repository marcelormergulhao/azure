
##

Show possible app service runtimes
az webapp list-runtimes --os-type linux

Show outbound IPs:

az webapp show \
    --resource-group <group_name> \
    --name <app_name> \ 
    --query outboundIpAddresses \
    --output tsv

Create new app:

az webapp up -g appservice-rg -n demoapp-mmergulhao --sku F1 --html

Set properties:

az webapp config appsettings set --resource-group appservice-rg --name demoapp-mmergulhao --settings somekey=somevalue another_key=another_value


## References

Demo HTML app for tests: https://github.com/Azure-Samples/html-docs-hello-world.git