# organization-deepcopy-demo
A script used for copying organization setup from a template organization to a fresh new organization.

## Brief introduction of the problem
There are multiple situations when you need to manage multiple organizations in Rossum:
* you are providing Rossum service to multiple customers and you would like to separate their data or give them more freedom by providing their users with the "Admin" role
* your company has multiple departments and you would like to separate the departments while providing high enough independence.

## How to manage multiple organizations in Rossum
In Rossum you can group organizations into an object [Organization group](https://api.elis.rossum.ai/docs/#organization-group). Within this group you can gather all the Rossum [organizations](https://api.elis.rossum.ai/docs/#organization). The organization group is created right when you create your first organization in Rossum.

If you would like to create multiple organizations within the same group, then you should request a [create_key](https://api.elis.rossum.ai/docs/#create-new-organization) for your Rossum organization groups.

For easier managemement of the organizations within the organization group we have prepared a new role "Organization group admin" that can:
1. All organizations within the org group
2. Get auth token to any organization within the organization group
3. Allow specific users (admins, annotators, managers) to access multiple organizations from the organization group

## Org group admin
The [organization group admin role](https://api.elis.rossum.ai/docs/#retrieve-all-membership-organizations) cannot be set over the API. Such a role can be setup for one of your users only by contacting the Rossum's UI. In the UI this user cannot be deactivated by any other user since the user is responsible for managing the whole organization group.

## What does deep-copy of an organization mean?
As an example of what the organization group means and what the organizaion group admin can do, we have prepared a script that:
1. Let's you create a new organization in given organization group
2. Lists all organizations in the given group and finds the one organization that is used as a "template"  organization in your org group.
3. Fetches all objects that should be copied from the template organization
4. Initializes the new organization to the same setup as the "template" organization

## Sharing other users among multiple organizations
Of course, more user roles can be shared among multiple organizations. E.g. admin user George can be assigned to the German and French department where he will check the setup of the organization. Please read [how to assign the user to another organization](https://api.elis.rossum.ai/docs/#create-new-membership). However, keep in mind that such action can be done only by organization group admin.

<a href="https://youtu.be/7MvitiSEp0I">Please watch a DEMO video showing how to manage the organizations here.</a>


