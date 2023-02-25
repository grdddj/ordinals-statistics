from bitcoin.rpc import RawProxy


def connection() -> RawProxy:
    return RawProxy(service_port=8332, btc_conf_file="mainnet.conf")
