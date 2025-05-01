FROM mcr.microsoft.com/cbl-mariner/base/core:2.0 as cm2
RUN tdnf install -y rpm-build make python3-devel
WORKDIR /src
RUN --mount=target=/src,rw make rpm && \
    mkdir /out && \
    cp -r /src/rpmbuild/RPMS/x86_64/*.rpm /out/

FROM mcr.microsoft.com/azurelinux/base/core:3.0 as azl3
RUN tdnf install -y rpm-build make python3-devel
WORKDIR /src
RUN --mount=target=/src,rw make rpm && \
    mkdir /out && \
    cp -r /src/rpmbuild/RPMS/x86_64/*.rpm /out/

FROM registry.access.redhat.com/ubi9:latest as el9
RUN yum install -y rpm-build make python3-devel
WORKDIR /src
RUN --mount=target=/src,rw make rpm && \
    mkdir /out && \
    cp -r /src/rpmbuild/RPMS/x86_64/*.rpm /out/

FROM registry.access.redhat.com/ubi8:latest as el8
RUN yum install -y rpm-build make python3-devel
WORKDIR /src
RUN --mount=target=/src,rw make rpm && \
    mkdir /out && \
    cp -r /src/rpmbuild/RPMS/x86_64/*.rpm /out/

FROM scratch
COPY --from=cm2 /out/* /
COPY --from=azl3 /out/* /
COPY --from=el8 /out/* /
COPY --from=el9 /out/* /
