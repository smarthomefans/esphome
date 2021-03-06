import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import display, spi
from esphome.const import (
    CONF_DC_PIN, CONF_ID, CONF_LAMBDA, CONF_PAGES, CONF_RESET_PIN, CONF_CS_PIN,
)

DEPENDENCIES = ['spi']

pcd8544_ns = cg.esphome_ns.namespace('pcd8544')
PCD8544 = pcd8544_ns.class_('PCD8544', cg.PollingComponent, display.DisplayBuffer, spi.SPIDevice)


CONFIG_SCHEMA = cv.All(display.FULL_DISPLAY_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(PCD8544),
    cv.Required(CONF_DC_PIN): pins.gpio_output_pin_schema,
    cv.Required(CONF_RESET_PIN): pins.gpio_output_pin_schema,
    cv.Required(CONF_CS_PIN): pins.gpio_output_pin_schema,  # CE
}).extend(cv.polling_component_schema('1s')).extend(spi.spi_device_schema()),
                       cv.has_at_most_one_key(CONF_PAGES, CONF_LAMBDA))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    yield cg.register_component(var, config)
    yield display.register_display(var, config)
    yield spi.register_spi_device(var, config)

    dc = yield cg.gpio_pin_expression(config[CONF_DC_PIN])
    cg.add(var.set_dc_pin(dc))
    reset = yield cg.gpio_pin_expression(config[CONF_RESET_PIN])
    cg.add(var.set_reset_pin(reset))

    if CONF_LAMBDA in config:
        lambda_ = yield cg.process_lambda(config[CONF_LAMBDA], [(display.DisplayBufferRef, 'it')],
                                          return_type=cg.void)
        cg.add(var.set_writer(lambda_))
