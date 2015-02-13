%define	oname	passenger

Summary:	Apache module for Ruby on Rails support
Name:		rubygem-%{oname}
Version:	3.0.5
Release:	9
License:	MIT
Group:		Development/Ruby
URL:		http://%{oname}.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{oname}-%{version}.gem
Source1:	mod_passenger.conf
Patch0:		rubygem-passenger-3.0.5-missing-includes.patch
Patch1:		rubygem-passenger-3.0.5-compile-flags.patch
BuildRequires:	ruby-devel ruby-RubyGems apache-devel ruby-rake
BuildRequires:	apache-base curl-devel
Provides:	apache-mod_passenger = %{version}-%{release}

%description
Passenger is an Apache module for Ruby on Rails support.

%prep
%setup -q
%patch0 -p1 -b .incs~
%patch1 -p1 -b .flags~

%build
%define _disable_ld_no_undefined 1
%setup_compile_flags
rake apache2 APXS2=%{_sbindir}/apxs OPTIMIZE=yes
%gem_build -f 'helper-scripts'

%install
install -m0644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/httpd/modules.d/mod_passenger.conf

%gem_install
install -m755 ext/apache2/mod_passenger.so -D %{buildroot}%{_libdir}/apache-extramodules/mod_passenger.so
install -m755 ext/ruby/ruby-*/passenger_native_support.so -D %{buildroot}%{ruby_sitearchdir}/passenger_native_support.so
cp -r agents  %{buildroot}%{ruby_sitearchdir}/
ln -s %{ruby_sitearchdir} %{buildroot}%{_prefix}/lib/phusion-passenger
install -d %{buildroot}%{_datadir}/phusion-passenger
ln -s %{ruby_gemdir}/gems/%{oname}-%{version}/helper-scripts %{buildroot}%{_datadir}/phusion-passenger

%post
service httpd condrestart

%postun
if [ "$1" = "0" ]; then
    service httpd condrestart
fi

%files
%defattr(-,root,root)
%doc %{ruby_gemdir}/doc/%{oname}-%{version}
%{gemdir}/gems/%{oname}-%{version}
%{gemdir}/specifications/%{oname}-%{version}.gemspec
%{ruby_sitearchdir}/passenger_native_support.so
%dir %{ruby_sitearchdir}/agents
%{ruby_sitearchdir}/agents/*
%{_bindir}/passenger*
%{_libdir}/apache-extramodules/mod_passenger.so
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/mod_passenger.conf
%{_prefix}/lib/phusion-passenger
%{_datadir}/phusion-passenger
