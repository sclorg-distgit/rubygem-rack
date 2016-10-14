%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name rack

Name:           %{?scl_prefix}rubygem-%{gem_name}
Summary:        Common API for connecting web frameworks, web servers and layers of software
# Introduce Epoch (related to bug 552972)
Epoch:          1
Version:        1.6.2
Release:        3%{?dist}
Group:          Development/Languages
# lib/rack/backports/uri/* are taken from Ruby which is (Ruby or BSD)
# lib/rack/show{status,exceptions}.rb contains snippets from Django under BSD license.
License:        MIT and (Ruby or BSD) and BSD
URL:            http://rack.github.io/
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0:         rack-1.6.2-multipart-limit-form-fields.patch
Requires:       %{?scl_prefix_ruby}ruby(rubygems)
Requires:       %{?scl_prefix_ruby}ruby(release)
BuildRequires:  %{?scl_prefix_ruby}ruby
BuildRequires:  %{?scl_prefix_ruby}rubygems-devel
BuildRequires:  %{?scl_prefix}rubygem(bacon)
BuildArch:      noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides:       bundled(okjson) = 20150104

%description
Rack provides a minimal, modular and adaptable interface for developing
web applications in Ruby.  By wrapping HTTP requests and responses in
the simplest way possible, it unifies and distills the API for web
servers, web frameworks, and software in between (the so-called
middleware) into a single method call.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}%{gem_instdir} -type f`; do
    [ ! -z "`head -n 1 $file | grep \"^#!\"`" ] && chmod -v 755 $file
done

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
bacon -Ilib --automatic --quiet
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%{gem_libdir}
%{gem_instdir}/bin
%{_bindir}/rackup
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/KNOWN-ISSUES
%doc %{gem_instdir}/HISTORY.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/SPEC
%doc %{gem_instdir}/example
%{gem_instdir}/test
%doc %{gem_instdir}/contrib

%changelog
* Fri Oct 14 2016 Dominic Cleal <dominic@cleal.org> 1.6.2-3
- Fix open file limit error from incorrect multipart counting (#814)

* Mon Dec 14 2015 Dominic Cleal <dcleal@redhat.com> 1.6.2-2
- Replace %%license for EL6 compatibility

* Wed Jun 17 2015 Vít Ondruch <vondruch@redhat.com> - 1:1.6.2-1
- Update to Rack 1.6.2.

* Tue Jun 2 2015 Steve Traylen <jstribny@redhat.com> - 1:1.6.1-1
- Update to 1.6.1

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 1:1.6.0-1
- Update to 1.6.0

* Thu Sep 25 2014 Steve Traylen <steve.traylen@cern.ch> - 1:1.5.2-4
- Add enable_check flag and disable check for .el7.
- Rely on autorequires and autoprovides.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 05 2014  Josef Stribny <jstribny@redhat.com> - 1:1.5.2-2
- Fix licensing
- Add virtual provide for bundled okjson

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 1:1.5.2-1
- Update to rack 1.5.2

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-3
- Enable thin test suite.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 08 2013 Josef Stribny <jstribny@redhat.com> - 1:1.4.5-1
- Update to Rack 1.4.5.

* Tue Jan 15 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.4-1
- Update to Rack 1.4.4.

* Thu Nov 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:1.4.1-2
- Fixed epoch in -doc sub-package.

* Mon Oct 29 2012 Vít Ondruch <vondruch@redhat.com> - 1:1.4.1-1
- Update to Rack 1.4.1.
- Documentation moved into subpackage.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.4.0-2
- Rebuilt for Ruby 1.9.3.

* Thu Jan 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.4.0-1
- Update to Rack 1.4.
- Moved gem install to %%prep to be able to apply patches.
- Applied two patches that fix test failures with Ruby 1.8.7-p357.

* Tue Jun 28 2011 Vít Ondruch <vondruch@redhat.com> - 1:1.3.0-1
- Updated to Rack 1.3.
- Fixed FTBFS.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.1.0-2
- Epoch 1 for keeping upgrade path from F-12 (related to bug 552972)
- Enable %%check

* Mon Jan  4 2010 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.1.0-1
- New upstream version

* Sun Oct 25 2009 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.0.1-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 26 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.0.0-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.9.1-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-2
- Remove unused macro (#470694)
- Add ruby(abi) = 1.8 as required by package guidelines (#470694)
- Move %%{gem_dir}/bin/rackup to %%{_bindir} (#470694)

* Sat Nov 08 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-1
- Initial package
