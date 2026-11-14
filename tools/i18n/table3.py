ROWS = {
"tr": [
 ("ZScaler", "Zscaler ZIA'da bir forwarding kuralı tanımlanır ve marketplace domain'leri proxy chaining ile AES proxy'sine iletilir."),
 ("BlueCoat", "Symantec ProxySG'de forwarding kuralları tanımlanır ve marketplace trafiği proxy chaining ile AES'e iletilir."),
 ("Netskope", "Netskope SWG trafik yolunda kalır ve marketplace domain'lerini upstream proxy olarak AES'e iletir (proxy chaining). Alternatif olarak bu domain'ler Netskope steering kurallarının dışında bırakılır ve PAC dosyasıyla doğrudan AES proxy'sine yönlendirilir (bypass)."),
 ("Prisma Access", "PAC dosyası, GlobalProtect'in Tunnel + Proxy ya da Proxy (Explicit Proxy) modunda Prisma Access forwarding profile'ı üzerinden dağıtılır."),
 ("Cloudflare", "Cloudflare Zero Trust'ta bir DNS override ya da egress policy ile marketplace domain'leri AES proxy'sine yönlendirilir."),
 ("Cisco Umbrella", "Marketplace domain'leri Umbrella'da External Domains olarak tanımlanıp SWG'nin dışında bırakılır; Umbrella'ya yüklenen PAC dosyası bu trafiği AES'e gönderir."),
 ("Fortinet", "FortiGate, marketplace trafiğini proxy chaining ya da explicit proxy ile AES proxy'sine iletir."),
 ("Global protect", "GlobalProtect Tunnel-only modunda çalışıyorsa PAC dosyası endpoint'lere ayrıca dağıtılır."),
 ("None of these (PAC file)", "Ortamda bu ürünlerden hiçbiri yoksa marketplace domain'leri bir PAC dosyasıyla AES proxy'sine yönlendirilir. PAC dosyası tek başına ya da mevcut bir PAC dosyasına eklenerek kullanılabilir; elle, AES script package'ı ile ya da MDM ile dağıtılır. Bu workshop'ta bu yöntem kullanılır."),
],
"en": [
 ("ZScaler", "A forwarding rule is defined in Zscaler ZIA, and marketplace domains are forwarded to the AES proxy with proxy chaining."),
 ("BlueCoat", "Forwarding rules are defined in Symantec ProxySG, and marketplace traffic is forwarded to AES with proxy chaining."),
 ("Netskope", "Netskope SWG stays in the traffic path and forwards marketplace domains to AES as an upstream proxy (proxy chaining). Alternatively, these domains are excluded from Netskope steering rules and routed directly to the AES proxy with a PAC file (bypass)."),
 ("Prisma Access", "The PAC file is distributed through the Prisma Access forwarding profile in GlobalProtect Tunnel + Proxy or Proxy (Explicit Proxy) mode."),
 ("Cloudflare", "In Cloudflare Zero Trust, marketplace domains are routed to the AES proxy with a DNS override or an egress policy."),
 ("Cisco Umbrella", "Marketplace domains are defined as External Domains in Umbrella and excluded from the SWG; a PAC file uploaded to Umbrella sends this traffic to AES."),
 ("Fortinet", "FortiGate forwards marketplace traffic to the AES proxy with proxy chaining or explicit proxy."),
 ("Global protect", "If GlobalProtect runs in Tunnel-only mode, the PAC file is distributed to endpoints separately."),
 ("None of these (PAC file)", "If none of these products is in the environment, marketplace domains are routed to the AES proxy with a PAC file. The PAC file can be used on its own or merged into an existing PAC file, and is distributed manually, with the AES script package, or through MDM. This workshop uses this method."),
],
"ru": [
 ("ZScaler", "В Zscaler ZIA создаётся правило forwarding, и домены маркетплейсов передаются на прокси AES через proxy chaining."),
 ("BlueCoat", "В Symantec ProxySG создаются правила forwarding, и трафик маркетплейсов передаётся в AES через proxy chaining."),
 ("Netskope", "Netskope SWG остаётся на пути трафика и передаёт домены маркетплейсов в AES как upstream proxy (proxy chaining). Другой вариант: эти домены исключаются из правил steering Netskope и направляются напрямую на прокси AES с помощью PAC-файла (bypass)."),
 ("Prisma Access", "PAC-файл распространяется через forwarding profile Prisma Access в режиме GlobalProtect Tunnel + Proxy или Proxy (Explicit Proxy)."),
 ("Cloudflare", "В Cloudflare Zero Trust домены маркетплейсов направляются на прокси AES с помощью DNS override или egress policy."),
 ("Cisco Umbrella", "Домены маркетплейсов задаются в Umbrella как External Domains и исключаются из SWG; загруженный в Umbrella PAC-файл отправляет этот трафик в AES."),
 ("Fortinet", "FortiGate передаёт трафик маркетплейсов на прокси AES через proxy chaining или explicit proxy."),
 ("Global protect", "Если GlobalProtect работает в режиме Tunnel-only, PAC-файл распространяется на endpoint'ы отдельно."),
 ("None of these (PAC file)", "Если ни одного из этих продуктов в среде нет, домены маркетплейсов направляются на прокси AES с помощью PAC-файла. PAC-файл можно использовать отдельно или добавить в существующий PAC-файл; он распространяется вручную, через script package AES или через MDM. На этом воркшопе используется этот способ."),
],
}
import html
def tbody(lang):
    return "<tbody>" + "".join(f"<tr><td><strong>{html.escape(n, quote=False)}</strong></td><td>{html.escape(d)}</td></tr>" for n, d in ROWS[lang]) + "</tbody>"
