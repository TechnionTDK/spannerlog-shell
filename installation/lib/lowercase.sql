CREATE FUNCTION lowercase (s text)
    RETURNS TABLE (lower text)
AS $$

return (s.lower(), )

$$ LANGUAGE plpythonu;
