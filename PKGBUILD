pkgname=argond
pkgdesc='Script for the Argon One Raspberry Pi 4 case.'
pkgver='1.0'
pkgrel='1'
arch=(aarch64)

url="https://github.com/colinjmatt/$pkgname"
depends=('i2c-tools' 'python' 'python-gpiozero' 'python-rpi-gpio')

source=("https://github.com/colinjmatt/$pkgname/archive/refs/tags/v1.0.tar.gz")
sha256sums=('SKIP')

package() {
        cd "$srcdir/$pkgname-$pkgver"
        install -Dm755 "argononed.py" "$pkgdir/opt/argonone/bin/argononed.py"
        install -Dm755 "argonone-config" "$pkgdir/opt/argonone/bin/argonone-config"
        install -Dm644 "argononed.conf" "$pkgdir/opt/argonone/argononed.conf"
        install -Dm755 "argononed-poweroff.py" "$pkgdir/usr/lib/systemd/system-shutdown/$pkgname-poweroff"
        install -Dm644 "argononed.service" "$pkgdir/usr/lib/systemd/system/argond.service"
}
