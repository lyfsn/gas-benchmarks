.PHONY: prepare_tools clean

prepare_tools:
	if [ ! -d "nethermind" ]; then \
		git clone https://github.com/NethermindEth/nethermind nethermind; \
	fi
	dotnet build ./nethermind/tools/Nethermind.Tools.Kute -c Release -p:WarningLevel=0

clean:
	rm -rf nethermind