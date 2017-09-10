CREATE FUNCTION lower (s text)
    RETURNS TABLE (lowered text)
AS $$

yield [s.lower()]

$$ LANGUAGE plpythonu;
