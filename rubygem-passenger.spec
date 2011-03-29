%define	oname	passenger

Summary:	Apache module for Ruby on Rails support
Name:		rubygem-%{oname}
Version:	2.2.9
Release:	4
License:	MIT
Group:		Development/Ruby
URL:		http://%{oname}.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{oname}-%{version}.gem
Source1:	mod_passenger.conf
Patch0:		rubygem-passenger-2.2.9-missing-includes.patch
Patch1:		rubygem-passenger-2.2.9-compile-flags.patch
BuildRequires:	ruby-devel ruby-RubyGems apache-devel ruby-rake
BuildRequires:	apache-base
Requires:	ruby-rack ruby-rake rubygem-fastthread rails
Provides:	apache-mod_passenger = %{version}-%{release}

%description
Passenger is an Apache module for Ruby on Rails support.

%prep
%setup -q
%patch0 -p1 -b .missing_includes~
%patch1 -p1 -b .flags~

%build
%define _disable_ld_no_undefined 1
%setup_compile_flags
rake APXS2=%{_sbindir}/apxs OPTIMIZE=yes
%gem_build

%install
install -m0644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/httpd/modules.d/mod_passenger.conf

%gem_install
install -m755 ext/apache2/mod_passenger.so -D %{buildroot}%{_libdir}/apache-extramodules/mod_passenger.so
install -m755 ext/apache2/ApplicationPoolServerExecutable -D %{buildroot}%{ruby_sitearchdir}/phusion_passenger/ApplicationPoolServerExecutable
#fixme:
mv %{buildroot}%{ruby_sitearchdir}/native_support.so %{buildroot}%{ruby_sitearchdir}/phusion_passenger/native_support.so
install -m755 ext/nginx/HelperServer -D %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/ext/nginx/HelperServer
ln -s %{ruby_sitearchdir}/phusion_passenger %{buildroot}%{_prefix}/lib

%post
service httpd condrestart

%postun
if [ "$1" = "0" ]; then
    service httpd condrestart
fi

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

