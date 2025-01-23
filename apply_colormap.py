import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss


@ns.materialtree("Apply Colormap")
def apply_colormap():
    mi = ss.attribute(
        attribute_type=ss.Attribute.AttributeType.INSTANCER, attribute_name="cm_min"
    ).fac
    ma = ss.attribute(
        attribute_type=ss.Attribute.AttributeType.INSTANCER, attribute_name="cm_max"
    ).fac
    value = ss.attribute(
        attribute_type=ss.Attribute.AttributeType.GEOMETRY, attribute_name="cm_value"
    ).fac
    normalized = ss.map_range(
        data_type=ss.MapRange.DataType.FLOAT,
        value=value,
        from_min=mi,
        from_max=ma,
        to_min=0.0,
        to_max=1.0,
    )
    vec = ss.combine_xyz(x=0.5, y=normalized, z=1.0)
    image_texture = ss.image_texture(vector=vec)
    return ss.principled_bsdf(base_color=image_texture.color)


@ns.tree("Colormapped Mesh")
def colormapped_mesh(geometry: ns.Geometry, property_name: ns.String):
    stored = gs.store_named_attribute(
        data_type=gs.StoreNamedAttribute.DataType.FLOAT,
        name="cm_value",
        domain=gs.StoreNamedAttribute.Domain.POINT,
        value=gs.named_attribute(name=property_name).attribute,
        geometry=geometry,
    )
    stats = gs.attribute_statistic(
        geometry=stored, attribute=gs.named_attribute(name="cm_value").attribute
    )
    instances = gs.geometry_to_instance(geometry=[stored])
    stored = gs.store_named_attribute(
        data_type=gs.StoreNamedAttribute.DataType.FLOAT,
        name="cm_min",
        domain=gs.StoreNamedAttribute.Domain.INSTANCE,
        value=stats.min,
        geometry=instances,
    )
    stored = gs.store_named_attribute(
        data_type=gs.StoreNamedAttribute.DataType.FLOAT,
        name="cm_max",
        domain=gs.StoreNamedAttribute.Domain.INSTANCE,
        value=stats.max,
        geometry=stored,
    )
    return stored
