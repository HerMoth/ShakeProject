/dts-v1/;
/plugin/;

/ {
    compatible = "brcm,bcm2837B0";

    fragment@0 {
        target = <&uart0>;
        __overlay__ {
            pinctrl-names = "default";
            pinctrl-0 = <&uart0_pins>;

            status = "okay";
        };
    };

    fragment@1 {
        target = <&gpio>;
        __overlay__ {
            uart0_pins: uart0_pins {
                brcm,pins = <25 27>;
                brcm,function = <4 4>; /* ALT4 for UART0 TX/RX */
                brcm,pull = <2>; /* Pull-up */
            };
        };
    };
};
