# TrustCalculation

This work was done as a Bachelor Thesis at the Institute of Applied Information Technoloy (InIT) at the Zurich University of Applied Sciences (ZHAW).

# Abstract
Although the topic of Network Function Virtualization (NFV) and containerized services embedded therein is an already active research field and is becoming increasingly widespread in practice (e.g., 5G networks), the challenges in terms of security and threats still deserve more attention and research efforts. To counteract the issues to this aspect, this thesis deals with the question of whether and how the issue of trust assessment can be addressed in such infrastructures. Different trust models are reviewed, and the trust attributes used in the literature are analysed in more detail and evaluated based on the knowledge gained. The parameters are subsequently included in a trust calculation for the confidence analysis. Thresholds for the assessment into trustworthy and non-trustworthy will be defined. The approach of developing a Dynamic Trust Monitoring (DTM) solution that supervises the trustworthiness of containerized services in an NFV infrastructure was implemented using a DTM prototype. This prototype is able to perform evaluations based on the results of NFV infrastructures. By collecting and processing the trust parameters, the infrastructures are evaluated according to their trustworthiness. Tests on the monitored system provided information regarding the practical applicability of our prototype. It was found that the DTM is suitable as a basis for further development. Nevertheless, improvements are necessary to be able to use the system in a productive environment.

# Overview over Repository
*	.github			Files for GitHub Actions 
*	docker			Files for Docker deployment 
*	helm			  Files for deployment with helm 
*	src			    Code Files 
*	thesis			Files about our thesis 
    *	results		Our test results in Excel Files


# How to start
If needed the project can be used by following these steps:
* Clone Repository 
* change global parameters in main 
* make Dockerimage with dockerfile 
* deploy with helm in a Kubernetes cluster 
   use helm folder for that \
\
Unfortunately the automatic deployed dockerfile can't be used at the moment, because it has parameters in it, which only work for our test environmnent
