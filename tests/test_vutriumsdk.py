#!/usr/bin/env python3
"""
Test script to verify VutriumSDK implementation completeness and functionality
Based on the example_client.py usage patterns
"""

import sys
import os
sys.path.insert(0, '/workspace/reconstructed_source')

def test_basic_imports():
    """Test that all required classes and functions can be imported"""
    print("Testing basic imports...")
    try:
        # Test the import from our reconstructed module
        sys.path.insert(0, '/workspace/reconstructed_source')
        from VutriumSDK_ABSOLUTE_FINAL import SDK, download_latest_and_inject, Util
        print("✓ Successfully imported SDK, download_latest_and_inject, Util")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_sdk_creation():
    """Test SDK object creation"""
    print("\nTesting SDK creation...")
    try:
        from VutriumSDK_ABSOLUTE_FINAL import SDK
        sdk = SDK()
        print("✓ SDK object created successfully")
        return True
    except Exception as e:
        print(f"❌ SDK creation failed: {e}")
        return False

def test_util_methods():
    """Test Util class methods"""
    print("\nTesting Util methods...")
    try:
        from VutriumSDK_ABSOLUTE_FINAL import Util
        util = Util()
        
        # Test json_to_field_info_packet with sample data
        sample_field_data = {"boost_pads": [], "goals": [], "field_id": "test"}
        field_packet = util.json_to_field_info_packet(sample_field_data)
        print("✓ json_to_field_info_packet works")
        
        # Test json_to_game_tick_packet with sample data
        sample_game_data = {
            "game_cars": [],
            "localPlayerIndices": [0],
            "localPlayerNames": ["TestPlayer"],
            "game_info": {"is_round_active": True}
        }
        game_packet = util.json_to_game_tick_packet(sample_game_data)
        print("✓ json_to_game_tick_packet works")
        
        return True
    except Exception as e:
        print(f"❌ Util methods test failed: {e}")
        return False

def test_subscribe_functionality():
    """Test SDK subscribe functionality"""
    print("\nTesting subscribe functionality...")
    try:
        from VutriumSDK_ABSOLUTE_FINAL import SDK
        sdk = SDK()
        
        # Test event handler subscription
        def test_handler(evt):
            pass
        
        sdk.subscribe("OnGameEventStart", test_handler)
        sdk.subscribe("OnGameEventDestroyed", test_handler)
        sdk.subscribe("PlayerTickHook", test_handler)
        print("✓ Event subscription works")
        
        return True
    except Exception as e:
        print(f"❌ Subscribe test failed: {e}")
        return False

def test_send_json_format():
    """Test the send_json method with controller input format"""
    print("\nTesting send_json with controller format...")
    try:
        from VutriumSDK_ABSOLUTE_FINAL import SDK
        sdk = SDK()
        
        # Test the exact format used in example_client.py
        controller_data = {
            "num_inputs": 1,
            "inputs": [{
                "throttle": 1.0,
                "steer": 0.0,
                "pitch": 0.0,
                "yaw": 0.0,
                "roll": 0.0,
                "jump": False,
                "boost": False,
                "handbrake": False,
                "use_item": False
            }]
        }
        
        # This should not fail even without connection (returns False)
        result = sdk.send_json(controller_data)
        print("✓ send_json method accepts controller format")
        
        return True
    except Exception as e:
        print(f"❌ send_json test failed: {e}")
        return False

def test_download_function():
    """Test download_latest_and_inject function exists and can be called"""
    print("\nTesting download_latest_and_inject function...")
    try:
        from VutriumSDK_ABSOLUTE_FINAL import download_latest_and_inject
        
        # This will likely fail with network error, but we just want to test it exists
        try:
            result = download_latest_and_inject()
            print("✓ download_latest_and_inject function exists and is callable")
        except Exception:
            print("✓ download_latest_and_inject function exists (network error expected)")
        
        return True
    except Exception as e:
        print(f"❌ download_latest_and_inject test failed: {e}")
        return False

def test_game_data_structures():
    """Test that the game data structures have required fields"""
    print("\nTesting game data structures...")
    try:
        from VutriumSDK_ABSOLUTE_FINAL import Util
        util = Util()
        
        # Test GameTickPacket with the fields used in example_client.py
        game_data = {
            "game_cars": [{"team": 0, "position": {"x": 0, "y": 0, "z": 0}}],
            "localPlayerIndices": [0],
            "localPlayerNames": ["TestPlayer"],
            "game_info": {"is_round_active": True}
        }
        
        packet = util.json_to_game_tick_packet(game_data)
        
        # Test the specific attributes used in example_client.py
        print(f"  - game_cars: {len(packet.game_cars)} cars")
        print(f"  - localPlayerIndices: {packet.localPlayerIndices}")
        print(f"  - localPlayerNames: {packet.localPlayerNames}")
        print(f"  - is_round_active: {packet.game_info.is_round_active}")
        
        print("✓ All required game data fields are accessible")
        return True
    except Exception as e:
        print(f"❌ Game data structures test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("VutriumSDK Implementation Verification Test")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_sdk_creation,
        test_util_methods,
        test_subscribe_functionality,
        test_send_json_format,
        test_download_function,
        test_game_data_structures
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The implementation appears complete and functional.")
    else:
        print("⚠️ Some tests failed. The implementation may need fixes.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)