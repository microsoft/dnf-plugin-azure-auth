# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material

Summary:        DNF plugin for accessing repos in Azure Blob Storage via Azure AD
Name:           dnf-plugin-azure-auth
Version:        %%version%%
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/microsoft/dnf-plugin-azure-auth/
Source0:        %{name}-%{version}.tar.gz
%global debug_package %{nil}
Requires:       python3-dnf

%description
DNF plugin for accessing repos in Azure Blob Storage via Azure AD

%prep
%setup -q

%install
mkdir -p %{buildroot}%{python3_sitelib}/dnf-plugins/
mkdir -p %{buildroot}%{_sysconfdir}/dnf/plugins/
cp azure_auth.py %{buildroot}%{python3_sitelib}/dnf-plugins/
cp azure_auth.conf %{buildroot}%{_sysconfdir}/dnf/plugins/azure_auth.conf

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dnf/plugins/azure_auth.conf
%{python3_sitelib}/dnf-plugins/azure_auth.py
%{python3_sitelib}/dnf-plugins/__pycache__/azure_auth.*

%changelog

* Thu Sep 19 2024 Tom Fay <tomfay@microsoft.com> - 0.1.0-1
- Original version
