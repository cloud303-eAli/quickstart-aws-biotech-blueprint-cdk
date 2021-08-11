import os
import yaml 

templateStream = open('./templates/AwsBiotechBlueprint.template.yml', 'r')
templateData = yaml.load(templateStream)

for parameter in templateData['Parameters']:
    if templateData['Parameters'][parameter]['Description'].startswith( 'Artifact hash for asset'):
        templateData['Parameters'][parameter]['Metadata'] = {
            "cfn-lint" : {
                "config": {
                    "ignore_checks": ['E9010'],
                    "ignore_reasons": {
                        "E9010": "This parameter is created automatically by templates created with the AWS CDK that provides a checksum for customers to use if they need it.The developers of this Quick Start have no control over the behavior of the CDK."
                    }
                }
            }
        }        

for resource in templateData['Resources']:
    if templateData['Resources'][resource]['Metadata']['aws:cdk:path'] == 'AwsBiotechBlueprint/ClientVpn/VpnCertificateLambdaCustomResourceRole/DefaultPolicy/Resource':
        templateData['Resources'][resource]['Metadata']['cfn-lint'] = {
            "config": {
                "ignore_checks": ['EIAMPolicyWildcardResource', 'EIAMPolicyActionWildcard'],
                "ignore_reasons": {
                    "EIAMPolicyWildcardResource": "This particular role gives permission to a custom resource to create a certificate. We cannot provide a specific certificate ARN at deployment time as it does not yet exist."
                    , "EIAMPolicyActionWildcard": "The policy action wildcards in this policy are generated by the AWS CDK, which the developers of this Quick Start have no control over."
                }
                    
            }
        }
        
    if templateData['Resources'][resource]['Metadata']['aws:cdk:path'] == 'AwsBiotechBlueprint/ConfigPacks/CP-Operational-Best-Practices-for-HIPAA-Security' \
    or templateData['Resources'][resource]['Metadata']['aws:cdk:path'] == 'Operational-Best-Practices-for-NIST-CSF':
        templateData['Resources'][resource]['Metadata']['cfn-lint'] = {
            "config": {
                "ignore_checks": ['E9101'],
                "ignore_reasons": {
                    "E9101": "The references to master in this resource refer to EMR service naming. Until the EMR service changes its usage of the term, this needs to be an exception.",
                }
                    
            }
        }        


    
with open('./templates/AwsBiotechBlueprint.template.yml', 'w') as json_file:
    yaml.dump(templateData, json_file, indent=2)