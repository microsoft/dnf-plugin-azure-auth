# dnf-plugin-azure-auth

This is a [dnf](https://github.com/rpm-software-management/dnf) plugin for authenticating against yum/dnf repos in Azure Blob Storage using Azure AD.

It uses the az cli to authenticate against Azure AD, so can only be used with Azure Blob Storage accounts that are [configured to use Azure AD for authentication](https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory).

To configure this plugin to be used with a dnf repo, add an entry to `/etc/dnf/plugins/azure_auth.conf` with the following format:

```
[<repo-id>]
```
*<repo-id> is the repository ID in the [dnf/yum configuration](https://www.man7.org/linux/man-pages/man5/dnf.conf.5.html#top_of_page)*

*This plugin doesn't support cross-tenant authentication, if/when this is added the config will be extended so you can specify a tenant.*

## Pregenerated tokens

This plugin also supports the user providing a prenerated token in the environment variable `DNF_PLUGIN_AZURE_AUTH_TOKEN`.

When this is set, the plugin will not use the az cli to generate a token. This allows the plugin to be used in bootstrapping scenarios where the az cli is not available.

This option is not recommended for normal use.

## Installation

For AzureLinux, download the RPM from the releases, then install it with (t)dnf/yum.
Alternatively build the RPM from source for your target platform.

## Dependencies

This plugin uses the az cli rather than the Azure Python SDK identity library to avoid dependency management problems:
- the plugin has to install to system python where dnf runs, so has to be distributed as an RPM
- azure-identity is not available as an RPM on all desired OSs (there is an AzureLinux azure-sdk RPM but it is 100s of MB)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
