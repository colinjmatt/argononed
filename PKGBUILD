pkgname=argononed
pkgdesc='Script for the Argon One Raspberry Pi 4 case.'
pkgver='latest'
pkgrel='1'
arch=('aarch64')

url="https://github.com/colinjmatt/$pkgname"
depends=('i2c-tools' 'python')

source=('argononed.py'
        'argonone-config'
        'argononed.conf'
        'argononed-poweroff.py'
        'argononed.service')

sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
        install -Dm755 "$srcdir/argononed.py" "$pkgdir/opt/argonone/bin/argononed.py"
        install -Dm755 "$srcdir/argonone-config" "$pkgdir/usr/bin/argonone-config"
        install -Dm644 "$srcdir/argononed.conf" "$pkgdir/opt/argonone/argononed.conf"
        install -Dm755 "$srcdir/argononed-poweroff.py" "$pkgdir/usr/lib/systemd/system-shutdown/$pkgname-poweroff"
        install -Dm644 "$srcdir/argononed.service" "$pkgdir/usr/lib/systemd/system/argond.service"
}