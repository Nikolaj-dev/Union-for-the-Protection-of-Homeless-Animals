import pytest
from datetime import datetime
from .orm import AdvertisementRepository, ShelterRepository, AnimalRepository


@pytest.mark.asyncio_cooperative
async def test_advertisement_repository():
    # Initialize repository
    repository = AdvertisementRepository()

    # Create an advertisement for testing
    advertisement_data = {
        "title": "Test Advertisement",
        "body": "This is a test advertisement.",
        "image_path": "/images/test_image.jpg",
        "published_time": datetime.now(),
    }
    await repository.create(**advertisement_data)

    # Retrieve the advertisement by title
    retrieved_advertisements = await repository.filter_all({"title": "Test Advertisement"})

    # Check if at least one advertisement is retrieved
    assert len(retrieved_advertisements) >= 1

    # Check if the retrieved advertisement matches the created advertisement
    retrieved_advertisement = retrieved_advertisements[-1]
    for key, value in advertisement_data.items():
        if key == "published_time":
            # Compare the datetime objects directly
            assert retrieved_advertisement.get(key) == value.strftime("%Y-%m-%d %I:%M %p")
        else:
            assert retrieved_advertisement.get(key) == value

    # Test retrieve_one method
    retrieved_one = await repository.retrieve_one(retrieved_advertisement['pk'])
    assert retrieved_one == retrieved_advertisement

    # Test retrieve_all method
    all_advertisements = await repository.retrieve_all()
    assert len(all_advertisements) >= 1

    # Test filter_all method
    filtered_advertisements = await repository.filter_all({"title": "Test Advertisement"})
    assert len(filtered_advertisements) >= 1

    # Test filter_by_time method
    days = 7  # Adjust the number of days as needed
    time_filtered_advertisements = await repository.filter_by_time(days)
    assert len(time_filtered_advertisements) >= 1

    # Test update method
    updated_data = {"title": "Updated Title"}
    await repository.update(retrieved_advertisement['pk'], updated_data)
    updated_advertisement = await repository.retrieve_one(retrieved_advertisement['pk'])
    assert updated_advertisement["title"] == updated_data["title"]

    # Test delete method
    await repository.delete(retrieved_advertisement['pk'])
    deleted_advertisement = await repository.retrieve_one(retrieved_advertisement['pk'])
    assert "message" in deleted_advertisement and "not found" in deleted_advertisement["message"]


@pytest.mark.asyncio_cooperative
async def test_shelter_repository():
    repository = ShelterRepository()

    # Create a shelter for testing
    shelter_data = {
        "title": "Test Shelter",
        "address": "Test Location",
        "phone_number": "+77005004455"
    }
    await repository.create(**shelter_data)

    # Retrieve the shelter by title
    retrieved_shelters = await repository.filter_all({"title": "Test Shelter"})

    # Check if at least one shelter is retrieved
    assert len(retrieved_shelters) >= 1

    # Check if the retrieved shelter matches the created shelter
    retrieved_shelter = retrieved_shelters[-1]
    for key, value in shelter_data.items():
        if key == "since_time":
            assert retrieved_shelter.get(key) == value.strftime("%Y-%m-%d %I:%M %p")
        else:
            assert retrieved_shelter.get(key) == value

    # Test retrieve_one method
    retrieved_one = await repository.retrieve_one(retrieved_shelter['pk'])
    assert retrieved_one == retrieved_shelter

    # Test retrieve_all method
    all_shelters = await repository.retrieve_all()
    assert len(all_shelters) >= 1

    # Test filter_all method
    filtered_shelters = await repository.filter_all({"title": "Test Shelter"})
    assert len(filtered_shelters) >= 1

    # Test update method
    updated_data = {"title": "Updated Shelter Name"}
    await repository.update(retrieved_shelter['pk'], updated_data)
    updated_shelter = await repository.retrieve_one(retrieved_shelter['pk'])
    assert updated_shelter["title"] == updated_data["title"]

    # Test delete method
    await repository.delete(retrieved_shelter['pk'])
    deleted_shelter = await repository.retrieve_one(retrieved_shelter['pk'])
    assert "message" in deleted_shelter and "not found" in deleted_shelter["message"]


@pytest.mark.asyncio_cooperative
async def test_animal_repository():
    repository = AnimalRepository()

    # Create an animal for testing
    animal_data = {
        "name": "Test Animal",
        "sex": "female",  # Replace with a valid sex value
        "age": 2,
        "species": "cat",  # Replace with a valid species value
        "since_time": datetime.now(),
        "shelter_id": 4,  # Replace with a valid shelter_id if needed
    }
    await repository.create(**animal_data)

    # Retrieve the animal by name
    retrieved_animals = await repository.filter_all({"name": "Test Animal"})

    # Check if at least one animal is retrieved
    assert len(retrieved_animals) >= 1

    # Check if the retrieved animal matches the created animal
    retrieved_animal = retrieved_animals[-1]
    for key, value in animal_data.items():
        if key == "since_time":
            assert retrieved_animal.get(key) == value.strftime("%Y-%m-%d %I:%M %p")
        else:
            assert retrieved_animal.get(key) == value

    # Test retrieve_one method
    retrieved_one = await repository.retrieve_one(retrieved_animal['pk'])
    assert retrieved_one == retrieved_animal

    # Test retrieve_all method
    all_animals = await repository.retrieve_all()
    assert len(all_animals) >= 1

    # Test filter_all method
    filtered_animals = await repository.filter_all({"name": "Test Animal"})
    assert len(filtered_animals) >= 1

    # Test update method
    updated_data = {"name": "Updated Animal Name"}
    await repository.update(retrieved_animal['pk'], updated_data)
    updated_animal = await repository.retrieve_one(retrieved_animal['pk'])
    assert updated_animal["name"] == updated_data["name"]

    # Test delete method
    await repository.delete(retrieved_animal['pk'])
    deleted_animal = await repository.retrieve_one(retrieved_animal['pk'])
    assert "message" in deleted_animal and "not found" in deleted_animal["message"]


if __name__ == "__main__":
    pytest.main()
