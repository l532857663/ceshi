.PHONY: all test doc exe mips

target = all_server

pkg = wifilz_server_config

all:
	@for CmdName in $(target); \
	do \
	GOPATH=`pwd` go build -o ./bin/$$CmdName ./src/cmd/$$CmdName.go; \
	done

test:
	@for PkgName in $(pkg); \
	do \
	GOPATH=`pwd` go test $$PkgName -v; \
	done

doc:
	@for PkgName in $(pkg); \
	do \
	mkdir -p doc/$$PkgName; \
	GOPATH=`pwd` godoc cmd/$$PkgName > doc/$$PkgName/$$PkgName.txt; \
	done

exe:
	mkdir ./bin/exe
	@for CmdName in $(target); \
	do \
	GOPATH=`pwd` CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o ./bin/exe/$$CmdName ./src/cmd/$$CmdName; \
	done

mips:
	mkdir ./bin/mips
	@for CmdName in $(target); \
	do \
	GOPATH=`pwd` CGO_ENABLED=0 GOOS=linux GOARCH=mips go build -o ./bin/mips/$$CmdName ./src/cmd/$$CmdName; \
	done

clean:
	rm -rfdv ./bin/*

clean_doc:
	rm -rfdv ./doc/*
