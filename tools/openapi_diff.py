import sys
import yaml
import requests

def main():
    # SSoT contract
    with open("api-contracts.yaml", "r", encoding="utf-8") as f:
        contract = yaml.safe_load(f)
    
    # Live OpenAPI
    resp = requests.get("http://127.0.0.1:8000/openapi.json")
    resp.raise_for_status()
    live = resp.json()
    
    contract_paths = set(contract["paths"].keys())
    live_paths = set(live["paths"].keys())
    
    # Diff
    missing = sorted(contract_paths - live_paths)
    extra = sorted(live_paths - contract_paths)
    present = sorted(contract_paths & live_paths)
    
    # CSV
    with open("openapi-diff.csv", "w", encoding="utf-8") as out:
        out.write("status,path,method,operationId\n")
        
        for p in missing:
            for method, spec in contract["paths"][p].items():
                if method in ["get","post","put","delete","patch"]:
                    op = spec.get("operationId", "")
                    out.write(f'MISSING,"{p}",{method.upper()},{op}\n')
        
        for p in extra:
            for method in live["paths"][p].keys():
                if method in ["get","post","put","delete","patch"]:
                    op = live["paths"][p][method].get("operationId", "")
                    out.write(f'EXTRA,"{p}",{method.upper()},{op}\n')
        
        for p in present:
            for method, spec in contract["paths"][p].items():
                if method in ["get","post","put","delete","patch"]:
                    op = spec.get("operationId", "")
                    out.write(f'OK,"{p}",{method.upper()},{op}\n')
    
    print(f"✓ openapi-diff.csv: {len(missing)} missing, {len(extra)} extra, {len(present)} ok")

if __name__ == "__main__":
    main()
