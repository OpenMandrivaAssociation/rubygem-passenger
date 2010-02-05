%define	oname	passenger

Summary:	Apache module for Ruby on Rails support
Name:		rubygem-%{oname}
Version:	2.2.9
Release:	%mkrel 1
License:	MIT
Group:		Development/Ruby
URL:		http://%{oname}.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{oname}-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ruby-devel ruby-RubyGems
Requires:	rubygem-rack rubygem-rake rubygem-fastthread

%description
Passenger is an Apache module for Ruby on Rails support.

%prep

%build

%install
rm -rf %{buildroot}
gem install --local --install-dir %{buildroot}/%{ruby_gemdir} --force %{SOURCE0}

rm -rf %{buildroot}%{ruby_gemdir}/{cache,gems/%{oname}-%{version}/ext}
mv %{buildroot}%{ruby_gemdir}/bin %{buildroot}%{_prefix}
sed -e 's#/usr/bin/ruby1.8#/usr/bin/env ruby#g' \
	-i %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/test/stub/rails_apps/mycook/public/dispatch.{rb,fcgi,cgi}
sed -e 's#ruby1.8#ruby#g' -i %{buildroot}%{_bindir}/passenger-memory-stats

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{ruby_gemdir}/doc/%{oname}-%{version}
%{ruby_gemdir}/gems/%{oname}-%{version}
%{ruby_gemdir}/specifications/%{oname}-%{version}.gemspec
%{_bindir}/passenger-*

