# organization-deepcopy-demo
A script used for copying organization setup from a template organization to a fresh new organization.

## Why would you need to manage multiple organizations in Rossum?
There are multiple situations when you need to manage multiple organizations in Rossum:
* you are providing Rossum service to multiple customers and you would like to separate their data or give them more freedom by providing their users with the "Admin" role
* your company has multiple departments and you would like to separate the departments while providing high enough independence.

## How to manage multiple organizations in Rossum
In Rossum you can group organizations into an object [Organization group](https://api.elis.rossum.ai/docs/#organization-group). Within this group you can gather all the Rossum [organizations](https://api.elis.rossum.ai/docs/#organization). The organization group is created right when you create your first organization in Rossum.

If you would like to create multiple organizations within the same group, then you should request a [create_key](https://api.elis.rossum.ai/docs/#create-new-organization) for your Rossum organization groups.

For easier managemement of the organizations within the organization group we have prepared a new role "Organization group admin" that can:
1. See all organizations within the org group
2. Get auth [token to any organization within the organization group](https://api.elis.rossum.ai/docs/#generate-a-token-to-access-the-organization) (with the auth token from the users primary organization)
3. Allow specific users (admins, annotators, managers) to access multiple organizations from the organization group

## Org group admin
Organization group admin is a user who can access all the organizations in the organization group by default. The [organization group admin role](https://api.elis.rossum.ai/docs/#retrieve-all-membership-organizations) cannot be set over the API. Such a role can be setup for one of your users only by contacting your Rossum's key point of contact. In the UI this user cannot be deactivated by any other user since the user is responsible for managing the whole organization group.

## What does deep-copy of an organization mean?
As an example of what the organization group means and what the organizaion group admin can do, we have prepared a script that:
1. Let's you create a new organization in given organization group
2. Lists all organizations in the given group and finds the one organization that is used as a "template"  organization in your org group.
3. Fetches all objects that should be copied from the template organization
4. Initializes the new organization to the same setup as the "template" organization

Example of the config for running the script:
```
python orgs_deep_copy_scripy.py --org_name "German department" --username "myusername@email.ai" --email "myusername@email.ai" --password "<YOUR_PASSWORD>" --create_key "<YOUR_ORG_GROUP_CREATE_KEY>" --token "<YOUR_USER_AUTH_TOKEN>"
```

## Sharing other users among multiple organizations
Of course, more user roles can be shared among multiple organizations. E.g. admin user George can be assigned to the German and French department where he will check the setup of the organization. Please read [how to assign the user to another organization](https://api.elis.rossum.ai/docs/#create-new-membership). However, keep in mind that such action can be done only by organization group admin.

![Users in multiple organizations](https://ibb.co/BrsG0DQ)

<a href="https://www.youtube.com/embed/7MvitiSEp0I">Please watch a video about Sharing of users in Rossum here</a> 

## How to get billing data for each organization
If you would like to get the billing data for each organization for a specific time rage, use Rossum's [billing endpoint](https://api.elis.rossum.ai/docs/#billing-for-organization) which can happily provide you with such information.
