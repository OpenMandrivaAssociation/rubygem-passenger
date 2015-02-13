%define	oname	passenger

Summary:	Apache module for Ruby on Rails support
Name:		rubygem-%{oname}
Version:	4.0.59
Release:	1
License:	MIT
Group:		Development/Ruby
URL:		http://%{oname}.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{oname}-%{version}.gem
Source1:	mod_passenger.conf
BuildRequires:	ruby-devel ruby-RubyGems apache-devel ruby-rake
BuildRequires:	apache-base curl-devel
Provides:	apache-mod_passenger = %{version}-%{release}

%description
Passenger is an Apache module for Ruby on Rails support.

%prep
%setup -q

%build
%define _disable_ld_no_undefined 1
%setup_compile_flags

export CC=gcc
export CXX=g++

export EXTRA_CXXFLAGS=$CXXFLAGS
export EXTRA_LDFLAGS=$LDFLAGS

rake apache2 APXS2=%{_bindir}/apxs OPTIMIZE=yes
%gem_build -f 'helper-scripts'

%install
install -m0644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/httpd/modules.d/mod_passenger.conf

%gem_install
install -m755 buildout/apache2/mod_passenger.so -D %{buildroot}%{_libdir}/apache-extramodules/mod_passenger.so
install -m755 buildout/ruby/ruby-*/passenger_native_support.so -D %{buildroot}%{ruby_sitearchdir}/passenger_native_support.so
cp -r buildout/agents  %{buildroot}%{ruby_sitearchdir}/
ln -s %{ruby_sitearchdir} %{buildroot}%{_prefix}/lib/phusion-passenger
install -d %{buildroot}%{_datadir}/phusion-passenger
ln -s %{gem_dir}/gems/%{oname}-%{version}/helper-scripts %{buildroot}%{_datadir}/phusion-passenger

%post
service httpd condrestart

%postun
if [ "$1" = "0" ]; then
    service httpd condrestart
fi

%files
%defattr(-,root,root)
%doc %{gem_dir}/doc/%{oname}-%{version}
%{gem_dir}/gems/%{oname}-%{version}
%{gem_dir}/specifications/%{oname}-%{version}.gemspec
%{ruby_sitearchdir}/passenger_native_support.so
%dir %{ruby_sitearchdir}/agents
%{ruby_sitearchdir}/agents/*
%{_bindir}/passenger*
%{_libdir}/apache-extramodules/mod_passenger.so
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/mod_passenger.conf
%{_prefix}/lib/phusion-passenger
%{_datadir}/phusion-passenger
