# Please review: | Generally this is the styling I try to follow:
- [Google: Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Google: Javascript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [Google: HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)

# Forking
Forking of this repo is allowed, and highly encouraged. The only thing I ask you do is give credit to me as the original author/designer. That being said though, if you make some absolutely fantastic changes and would like to create a formatted pull request, I will gladly give you credit for features where it is due!

# Pull Requests
If you find yourself fixing a bug in this project, or adding useful features off of your fork/clone/whatever, please feel free to submit a pull request! However, I ask you follow this format to keep things organized. 

- Your pull request title must be: `Developer Pull Request: #<Fixed Issue ID>-<branch-name>; <any other details>`
    * IE: `Developer Pull Request: #8-add-forums; Also fixes #2`
    * If there is not an issue for your pull request: 
        `Developer Pull Request: <branch-name>: <branch-description>; <any other details>`
        IE: `Developer Pull Request: 12-toastr-msgs: Adds toastr messages for channels;`
- You must attach the corresponding labels for the changes made in your pull-request.
    * IE: If you're adding S3 Storage capabilities add the `storage` label. There are many other labels that 
    apply here too such as `CORE` since we'll be adding another storage backend ( Modification to Main/Settings 
    ), and the `project` label, since it affects the entire project.
- Post a checklist summary of your changes, with details on what it does. IE:
    - [ ] Add Django-Storages for S3 capability 
    - [ ] S3 ENV vars added to .env
    - [ ] Add code to enable S3 backend if .env vars for S3 are present.
- Post at least one gif/picture/video of the affects of your changes; IE: Demo'ing a change to the user-interface, or a bug fix.
- If you didn't already, you must include py-test tests for your changes.
- Your changes must pass CircleCI tests.

Once you meet this format, your pull-request will be reviewed/nit-picked for style integration/etc, staged, and then merged in if testing successfully with staging. Style integration is important to me, because an often used golden rule for programming is: "A project should always look like it was coded by one person, no matter the number of contributors" and I agree with this very much as it improves comprehension/understanding, or at least that's my opinion on the matter.

Thanks for reading and following this format/guide! 
