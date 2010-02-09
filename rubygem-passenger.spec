%define	oname	passenger

Summary:	Apache module for Ruby on Rails support
Name:		rubygem-%{oname}
Version:	2.2.9
Release:	%mkrel 2
License:	MIT
Group:		Development/Ruby
URL:		http://%{oname}.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{oname}-%{version}.gem
Source1:	mod_passenger.conf
Patch0:		rubygem-passenger-2.2.9-missing-includes.patch
Patch1:		rubygem-passenger-2.2.9-compile-flags.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ruby-devel ruby-RubyGems apache-devel ruby-rake
Requires:	ruby-rack ruby-rake rubygem-fastthread rails
Provides:	apache-mod_passenger = %{version}-%{release}

%description
Passenger is an Apache module for Ruby on Rails support.

%prep
%setup -q -c -T -n %{oname}-%{version}
gem unpack %{SOURCE0} --target %{_builddir}
%patch0 -p1 -b .missing_includes~
%patch1 -p1 -b .flags~

%build
%define _disable_ld_no_undefined 1
%setup_compile_flags
rake APXS2=%{_sbindir}/apxs OPTIMIZE=yes

%install
rm -rf %{buildroot}
install -m0644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/httpd/modules.d/mod_passenger.conf

gem install --bindir %{buildroot}%{_bindir} --local --install-dir %{buildroot}/%{ruby_gemdir} --force %{SOURCE0}

rm -rf %{buildroot}%{ruby_gemdir}/{cache,gems/%{oname}-%{version}/{debian,ext}}
find %{buildroot} -name passenger-install-apache2-module -o -name passenger-install-nginx-module |xargs rm -f
sed -e 's#/usr/bin/ruby1.8#/usr/bin/env ruby#g' \
	-i %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/test/stub/rails_apps/mycook/public/dispatch.{rb,fcgi,cgi}
sed -e 's#ruby1.8#ruby#g' -i %{buildroot}%{_bindir}/passenger-memory-stats

install -m755 ext/apache2/mod_passenger.so -D %{buildroot}%{_libdir}/apache-extramodules/mod_passenger.so
install -m755 ext/apache2/ApplicationPoolServerExecutable -D %{buildroot}%{ruby_sitearchdir}/phusion_passenger/ApplicationPoolServerExecutable
install -m755 ext/phusion_passenger/native_support.so -D %{buildroot}%{ruby_sitearchdir}/phusion_passenger/native_support.so
install -m755 ext/nginx/HelperServer -D %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/ext/nginx/HelperServer
ln -s %{ruby_sitearchdir}/phusion_passenger %{buildroot}%{_prefix}/lib

%post
service httpd condrestart

%postun
if [ "$1" = "0" ]; then
    service httpd condrestart
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{ruby_gemdir}/doc/%{oname}-%{version}
%{ruby_gemdir}/gems/%{oname}-%{version}
%{ruby_gemdir}/specifications/%{oname}-%{version}.gemspec
%dir %{ruby_sitearchdir}/phusion_passenger
%{ruby_sitearchdir}/phusion_passenger/ApplicationPoolServerExecutable
%{ruby_sitearchdir}/phusion_passenger/native_support.so
%{_bindir}/passenger-*
%{_libdir}/apache-extramodules/mod_passenger.so
%{_prefix}/lib/phusion_passenger
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/mod_passenger.conf

