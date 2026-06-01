pkgname=argond
pkgdesc='Script for the Argon One Raspberry Pi 4 case.'
pkgver='1.0'
pkgrel='1'
arch=(aarch64)

url="https://github.com/colinjmatt/$pkgname"
depends=(i2c-tools python python-gpiozero)

source=("https://github.com/colinjmatt/$pkgname/archive/v$pkgver.tar.gz")
sha256sums=(8e00fdc821e8b74d905232ad77013d4bd2178e41d6bb1991331f3cf8478bfe7c)

package() {
        cd "$srcdir/$pkgname-$pkgver"
        install -Dm755 "argononed.py" "$pkgdir/opt/argonone/bin/argononed.py"
        install -Dm755 "argonone-config" "$pkgdir/opt/argonone/bin/argonone-config"
        install -Dm644 "argononed.conf" "$pkgdir/opt/argonone/argononed.conf"
        install -Dm755 "argononed-poweroff.py" "$pkgdir/usr/lib/systemd/system-shutdown/$pkgname-poweroff"
        install -Dm644 "argononed.service" "$pkgdir/usr/lib/systemd/system/argond.service"
}
